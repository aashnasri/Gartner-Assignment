from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class output_generation:

  def __init__(self,user_query,
               retriever ,
               llm):
    
    self.user_query = user_query
    self.llm = llm
    self.retrieved_docs = retriever.invoke(input=self.user_query)
    self.retrieved_docs = [doc.page_content for doc in self.retrieved_docs]
    self.retrieved_docs = "\n".join(self.retrieved_docs)
    self.retrieved_docs = self.retrieved_docs.replace("\n", " ")
    self.retrieved_docs = self.retrieved_docs.replace("  ", " ")

  def llm_call(self):
    prompt_template = ChatPromptTemplate.from_messages([
                  ("system", """You're a helpful assistant",
            "Use the following information as in Context to answer the user's question. ",
            "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. ",
            "If you don't know the answer based on context, just say that you don't know, don't try to make up an answer. ",
            "If you think user is asking a follow up question, you can take some historical information from history",
            "Context: {retrieved_docs} ",
            "",
            "Please generate answers from the context provided above only and return the output in a pretty format."""),
                  ("user", "{user_query}")
              ])

    # chat_llm = self.llm.get_gpt_llm()

    custom_chain =  prompt_template | self.llm | StrOutputParser()

    output = custom_chain.invoke({
              "retrieved_docs": self.retrieved_docs,
              "user_query": self.user_query,
          })

    return output
