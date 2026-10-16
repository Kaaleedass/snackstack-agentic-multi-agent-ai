
from langchain.agents import create_agent

from SnackStack.config import llm, get_logger
from SnackStack.Tools.menu_tools import search_menu_catalog

logger = get_logger("menu_agent")

menu_agent = create_agent(
    model=llm,
    tools=[search_menu_catalog],
    system_prompt=(
        "You are the SnackStack Menu Assistant. "
        "Help customers discover food from the available menu. "
        "Use the search_menu_catalog tool for menu questions. "
        "Recommend dishes based on ingredients, cuisine, and "
        "dietary preferences. Only state prices and availability "
        "supported by the tool results. If no suitable dish is "
        "found, explain that clearly. Be friendly and concise."
    ),
)


def ask_menu_agent(question: str) -> str:
    """Answer a customer's menu-related question."""
    logger.info("Customer menu question: %s", question)

    result = menu_agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return result["messages"][-1].content
