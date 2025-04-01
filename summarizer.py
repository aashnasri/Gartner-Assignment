import requests
import json

def summarize_text_with_huggingface(text, max_length=500, temperature=0.3, top_p=0.8):
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": "Bearer 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"}  

    prompt = f"""
    Please summarize the following story in a **concise and informative** manner and output should be a short summary as a paragraph with continuation:
    ---
    {text}
    ---
    Your summary should be **clear, factual, and under {max_length} words**.
    """
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "temperature": temperature,
            "top_p": top_p,
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    
    # Extract the generated text
    extracted_text = result[0]['generated_text'].split(f"{max_length} words**.", 1)[-1]
    return extracted_text

summary_book = ""