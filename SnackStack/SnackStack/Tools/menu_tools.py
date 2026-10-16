
from langchain.tools import tool

from SnackStack.rag import menu_vectorstore
from SnackStack.config import get_logger

logger = get_logger("menu_tools")


@tool
def search_menu_catalog(query: str) -> str:
    """Search the SnackStack menu for dishes matching a customer's request.

    Use this tool to find food by cuisine, ingredients, dietary
    preferences, descriptions, or other menu-related requirements.
    """

    results = menu_vectorstore.similarity_search(query, k=4)

    if not results:
        return "No matching dishes were found."

    return "\n\n".join(
        doc.page_content for doc in results
    )
