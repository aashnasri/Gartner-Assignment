from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Union, Any, Dict, Optional

class Chunker:
  def __init__(self,text : str) -> str:
    self.text = text

  def lang_chainrecursive_splitter(self,
                                   chunk_size : int,
                                   overlap : int ) -> List:
    text_splitter = RecursiveCharacterTextSplitter(
              chunk_size = chunk_size,
              chunk_overlap = overlap,
              separators=[
                        "\n\n", "\n",
                        " ", ".",
                        ",",
                        "\u200b",  # Zero-width space
                        "\uff0c",  # Fullwidth comma
                        "\u3001",  # Ideographic comma
                        "\uff0e",  # Fullwidth full stop
                        "\u3002",  # Ideographic full stop
                        "",
                    ],
          )
    chunks = text_splitter.split_text(self.text)
    # chunks = [Document(page_content=i,metadata={"chunkid": str(uuid.uuid4())}) for i in chunks]
    return chunks
