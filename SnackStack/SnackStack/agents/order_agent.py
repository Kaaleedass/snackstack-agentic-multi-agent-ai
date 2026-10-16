
"""
SnackStack Order Agent.
Handles order tracking and asks for missing identifiers.
"""

from langchain.agents import create_agent

from SnackStack.config import llm, get_logger
from SnackStack.Tools.order_tools import get_order_status

logger = get_logger("order_agent")

order_agent = create_agent(
    model=llm,
    tools=[get_order_status],
    system_prompt=(
        "You are the SnackStack Order Support Assistant. "
        "Help customers check their order status. "
        "Use the get_order_status tool whenever the customer "
        "provides an order ID, tracking ID, or email address. "
        "If no identifier is provided, politely ask the customer "
        "to provide one. Never invent order details. "
        "Keep your responses friendly and concise."
    ),
)


def ask_order_agent(question: str) -> str:
    """Answer an order-related question."""
    logger.info("Customer order question: %s", question)

    result = order_agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return result["messages"][-1].content
