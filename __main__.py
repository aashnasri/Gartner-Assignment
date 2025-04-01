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

def main():
    if find_dotenv():
        load_dotenv(override=True)

    # Download and load the book content
    book_content = download_and_load_book(
        'https://www.gutenberg.org/cache/epub/1342/pg1342.txt', '_temp/book.txt'
    )

    # Chunk the book content
    lang_chain_chunker = Chunker(book_content)
    chunks = lang_chain_chunker.lang_chainrecursive_splitter(50000, 50)

    summary_book = ""
    for i in chunks[:1]:
        summ = summarize_text_with_huggingface(i)
        summary_book += summ
        summary_book += "\n\n"

    ontology = generate_ontology_with_mistral(summary_book)

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

    # Set up retriever
    retriever_obj = retrieval(vec_db)
    similarity_retriever = retriever_obj.chroma_retriever()

    # Set up LLM
    chat_llm = ChatOpenAI(
        model_name='gpt-4o',
        temperature=0.0,
        max_tokens=126
    )

    # Generate output
    result = output_generation(
        "who os daughter of Catherine", similarity_retriever, chat_llm
    ).llm_call()

    print(result)


if __name__ == "__main__":
    main()
