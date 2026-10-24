from src.embeddings.base_embedder import BaseEmbedder
from src.embeddings.openai_embedder import OpenAIEmbedder
from src.embeddings.huggingface_embedder import HuggingFaceEmbedder


def create_embedder(provider: str = "openai", **kwargs):
    if provider == "openai":
        return OpenAIEmbedder(**kwargs)
    elif provider == "huggingface":
        return HuggingFaceEmbedder(**kwargs)
    else:
        raise ValueError(f"UnSupported embedder provider: {provider}")
