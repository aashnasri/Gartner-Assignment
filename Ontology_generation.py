import requests
import json
import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Define the Mistral API details


def trim_string(input_string: str) -> str:
    start_index = input_string.find('{')
    end_index = input_string.rfind('}')
    
    if start_index != -1 and end_index != -1 and start_index < end_index:
        return input_string[start_index:end_index + 1]
    else:
        return '' 


def query_mistral(prompt, max_length=500, temperature=0.3, top_p=0.8):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": "Bearer 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"}

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "temperature": temperature,
            "top_p": top_p,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to generate ontology using Mistral
def generate_ontology_with_mistral(summary):
    prompt = f"""
    Extract the entities, relationships, and attributes from the following story and create an ontology
    the output should include
    - entities: a list of entities with their name, type, and role
    - relationships: a list of relationships with subject, predicate, and object
    - attributes: a list of attributes with subject, attribute, and value
    {summary}
    ---
    Provide the ontology in JSON format.
    """
    result = query_mistral(prompt)

    ontology_text = result[0]['generated_text'].split("ontology in JSON format.", 1)[-1]
    result = trim_string(ontology_text)

    result = json.loads(result)
    return (result)

# ontology = generate_ontology_with_mistral(summary_book)