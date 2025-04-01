class retrieval:
    def __init__(self,db) -> None:
        self.vectordb = db

    def chroma_retriever(self, top_k : int = 2,search_type="similarity"):
        retriever = self.vectordb.as_retriever(search_type = search_type ,search_kwargs={ "k" : top_k})
        return retriever