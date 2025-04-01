# Gartner-Assignment

# Project Overview

This project is designed to handle various tasks such as dowloading txt files,  summarization, ontology generation,, and content generation using advanced language models. The workspace is structured to support modular development and includes components for chunking, embedding, downloading content, and more.

## Directory Structure

├── __main__.py # Entry point for the application 
├── .gitignore # Git ignore file 
├── ChromaDB.py # initialising ChromaDB 
├── Ontology_generation.py # Generates ontologies from input data using Mistral 7B model
├── requirements.txt # Python dependencies 
├── retriever.py # Retrieves relevant documents from the Chroma db using cosine similarity score
├── streamlit.py # Streamlit app for UI 
├── summarizer.py # summarises the text
├── testing.ipynb # Jupyter notebook for testing 
├── _temp/ # to store the user uploaded documents
│ └── book.txt # Example input file 
├── .devcontainer/ # Development container configuration 
│ └── devcontainer.json 
├── Chunking/ 
│ ├── chunker.py # Handles chunking of documents using Recursive text splitter from langchain
├── download_content/  
│ └── downloader.py # Downloads content from external sources
├── Embedding_methods/ # Embedding-related methods 
├── Generation/  
│ └── output_gen.py # Generates output using retrieved contents using GPT 4o 


## Key Components

### 1. **Document Downloading**
   - Implemented in download content file
   - Download the content in txt format from the weblink of the book provided by the user 
   - once downloaded txt file is saved /_temp folder

### 2. **Chunking**
    - Since the Downloaded content is too big, we will chunk the entire content to smaller documents so that llm can handle the chunks efficiently

### 3. **Summarization**
   - Implemented in [`summarizer.py`](summarizer.py).
   - Summarizes each of the chunk generated using chunker and will combine all the summaries of indiviudual chunks to regenerate the summary of the
     complete book.
   - The combined summary is used for creating ontology
   - Summary is genrated using Mistral 7B model      

### 4. **Ontology Generation**
   - Implemented in [`Ontology_generation.py`](Ontology_generation.py).
   - Generates ontologies from genrated summary

### 5. **Vector db setup**
   - Uses ChromaDB for efficient storage and retrieval.
   - Implemented in (ChromaDB.py).
   - Implemented Chroma db and store the generated ontology using OpenAI embeddings

### 6. **Document Retrieval**
   - Implemented in [`retriever.py`](retriever.py).
   - Retrieves relevant documents based on user queries.

### 7. **Content Generation**
   - Implemented in [`output_gen.py`](Generation/output_gen.py).
   - Uses language models to generate responses based on retrieved documents.

### 8. **Streamlit UI**
   - Implemented in [`streamlit.py`](streamlit.py).
   - Provides a user-friendly interface for interacting with the system.


