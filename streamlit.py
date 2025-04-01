import streamlit as st
from download_content.downloader import download_and_load_book
from Chunking.chunker import Chunker
from dotenv import load_dotenv, find_dotenv
from Embedding_methods.openai_embeddings import get_embedding
from ChromaDB import vectordb
from langchain_openai import ChatOpenAI
from retriever import retrieval
from Generation.output_gen import output_generation
from summarizer import summarize_text_with_huggingface
from Ontology_generation import generate_ontology_with_mistral
from langchain.schema import Document

# Load environment variables
if find_dotenv():
    load_dotenv(override=True)

# Streamlit app
st.title("Gartner Chatbot ")

# Input for book URL
book_url = st.text_input("Enter the URL of the book:")

# Input for question
question = st.text_input("Enter your question about the book:")

# Button to process
if st.button("Analyze"):
    with st.spinner("Downloading and processing the book..."):
        # Download and load book content
        book_content = download_and_load_book(book_url, '_temp/book.txt')

        # Chunk the book content
        lang_chain_chunker = Chunker(book_content)
        chunks = lang_chain_chunker.lang_chainrecursive_splitter(50000, 50)

        # Summarize the book
        summary_book = ""
        for i in chunks[:1]:
            summ = summarize_text_with_huggingface(i)
            summary_book += summ
            summary_book += "\n\n"

        # Generate ontology
        ontology = generate_ontology_with_mistral(summary_book)

        # Create documents from ontology
        documents = []
        for entity in ontology["entities"]:
            doc_text = f"Entity: {entity['name']}, Type: {entity['type']}, Role: {entity['role']}"
            documents.append(Document(page_content=doc_text, metadata={"type": "entity"}))

        for relation in ontology["relationships"]:
            doc_text = f"Relationship: {relation['subject']} {relation['predicate']} {relation['object']}"
            documents.append(Document(page_content=doc_text, metadata={"type": "relationship"}))

        for attribute in ontology["attributes"]:
            doc_text = f"Attribute: {attribute['subject']} is {attribute['attribute']} = {attribute['value']}"
            documents.append(Document(page_content=doc_text, metadata={"type": "attribute"}))

        # Generate embeddings
        embeddings = get_embedding()

        # Initialize vector database
        vdb = vectordb(embeddings)
        vec_db = vdb.chromadb(persist_directory='book_collection', collection_name='book')
        vec_db.add_documents(documents)

        # Create retriever
        retriever_obj = retrieval(vec_db)
        similarity_retriever = retriever_obj.chroma_retriever()

        # Initialize ChatOpenAI
        chat_llm = ChatOpenAI(
            model_name='gpt-4o',
            temperature=0.0,
            max_tokens=126
        )

        # Generate output
        result = output_generation(question, similarity_retriever, chat_llm).llm_call()

    st.success("Analysis complete!")
    st.write("### Answer:")
    st.write(result)
