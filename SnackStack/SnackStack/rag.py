"""
RAG: Build a ChromaDB vector store from the product catalog.

The vector store is created once at import time and re-used by the
search_product_catalog tool.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from SnackStack.config import embeddings, get_logger
from SnackStack.data.menu import menu_catalog



logger = get_logger("rag")


def _build_documents() -> list[Document]:
    """Convert every catalog entry into a LangChain Document."""
    docs: list[Document] = []
    for p in menu_catalog:
        content = (
            f"name: {p['name']}\n"
            f"Category: {p['category']}\n"
            f"price:{p['price']}\n"
            f"cuisine: {p['cuisine']}\n"
            f"Rating: {p['rating']}/5\n"
            f"dietary_tags:{p["dietary_tags"]},\n"
            f"Description: {p['description']}\n"
            f"availability: {'Yes' if p['availability'] else 'No'}"
        )
        docs.append(
            Document(
                page_content=content,
                metadata={
                    "id": p["id"],
                    "name": p["name"],
                    "category": p["category"],
                    "price": p["price"],
                    "rating": p["rating"],
                },
            )
        )
    return docs


def build_vectorstore() -> Chroma:
    """Create an in-memory ChromaDB collection from the product catalog."""
    docs = _build_documents()
    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="Menu_products",
    )
    logger.info("Vector store ready  (%d products indexed)", len(docs))
    return store


# Module-level singleton so every importer shares the same store
# Create the vector store once when this module is imported
menu_vectorstore = build_vectorstore()
