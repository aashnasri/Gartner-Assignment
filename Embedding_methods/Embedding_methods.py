from langchain_openai import OpenAIEmbeddings

def get_embedding(model="text-embedding-ada-002"):
  embeddings = OpenAIEmbeddings(model= model)
  return embeddings
