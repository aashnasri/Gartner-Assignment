import shutil
from langchain_community.vectorstores import Chroma
import os

class vectordb:
  '''
  Initialising various vector dbs  dc
  '''
  def __init__(self,
               embedding_model,
               full_load : bool = True):

    self.embedding_model = embedding_model
    self.full_load = full_load

  def _ischroma_persist(self,
                        persist_directory : str) -> None:
    """
    The function will clear the directory path if full load is required  
    """

    if self.full_load and os.path.exists(persist_directory):
      shutil.rmtree(persist_directory, ignore_errors=True)


  def chromadb(self,
               persist_directory : str,
               collection_name : str):
    '''
    Initialising Chroma db
    '''
    _ = self._ischroma_persist(persist_directory=persist_directory)

    vec_db = Chroma(embedding_function=self.embedding_model,collection_name=collection_name,persist_directory=persist_directory)
    return vec_db
  
  def chromadb_load(self, persist_directory: str):
    """
    Load an existing Chroma vector store from the persistence directory.
    """
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"The persistence directory '{persist_directory}' does not exist.")

    # Load the existing Chroma database
    vec_db = Chroma(embedding_function=self.embedding_model, persist_directory=persist_directory)
    return vec_db
  

