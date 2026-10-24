from typing import List
from langchain_openai import OpenAIEmbeddings
import os
from src.embeddings.base_embedder import BaseEmbedder

from dotenv import load_dotenv

load_dotenv()


class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, model: str = "text-embedding-3-small", **kwargs):
        self.model = model
        self.client = OpenAIEmbeddings(model=model, 
                                       api_key=os.getenv("OPENAI_API_KEY"), 
                                       base_url=os.getenv("BASE_URL"),
                                       **kwargs)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts=texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed_query(text=text)