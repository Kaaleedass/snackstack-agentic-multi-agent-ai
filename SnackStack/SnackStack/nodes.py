
import re
from typing import Literal

from langgraph.types import Command, Send, interrupt

from SnackStack.state import StackState
from SnackStack.agents.orchestrator import route_query
from SnackStack.agents.menu_agent import ask_menu_agent
from SnackStack.agents.order_agent import ask_order_agent
from SnackStack.agents.synthesizer import synthesize_response
from SnackStack.config import get_logger

logger = get_logger("nodes")


def orchestrator_node(
    state: StackState,
) -> Command[Literal["menu_agent", "order_agent", "synthesizer"]]:
    """Choose the agent or agents needed for the current question."""

    query = state["user_query"]
    decision = route_query(query)

    logger.info("Route selected: %s", decision.route)

    if decision.route == "menu":
        targets = [Send("menu_agent", {"user_query": query})]
    elif decision.route == "order":
        targets = [Send("order_agent", {"user_query": query})]
    else:
        targets = [
            Send("menu_agent", {"user_query": query}),
            Send("order_agent", {"user_query": query}),
        ]

    return Command(
        update={
            "route": decision.route,
            "reasoning": decision.reasoning,
        },
        goto=targets,
    )


def menu_node(state: StackState) -> Command[Literal["synthesizer"]]:
    """Run the menu agent."""

    answer = ask_menu_agent(state["user_query"])

    return Command(
        update={
            "agent_results": [
                {"source": "menu", "response": answer}
            ]
        },
        goto="synthesizer",
    )


def order_node(state: StackState) -> Command[Literal["synthesizer"]]:
    """Run the order agent, asking for an identifier if necessary."""

    query = state["user_query"]

    identifier_pattern = (
        r"\bORD-\d+\b"
        r"|\bSS\d+TRK\b"
        r"|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"
    )

    match = re.search(identifier_pattern, query, re.IGNORECASE)

    if not match:
        logger.info("Order identifier missing. Asking customer.")

        customer_identifier = interrupt(
            "Please provide your order ID (e.g., ORD-201), "
            "tracking ID (e.g., SS201TRK), "
            "or registered email address."
        )

        query = (
            f"{query}\n"
            f"Customer-provided identifier: {customer_identifier}"
        )
    else:
        logger.info("Order identifier found in customer query.")

    answer = ask_order_agent(query)

    return Command(
        update={
            "agent_results": [
                {"source": "order", "response": answer}
            ]
        },
        goto="synthesizer",
    )


def synthesizer_node(state: StackState) -> dict:
    """Return one agent's answer or combine both agents' answers."""

    results = state.get("agent_results", [])

    if not results:
        return {
            "final_answer": (
                "Sorry, I could not process your request. Please try again."
            )
        }

    # Use the latest result for each agent, if present.
    menu_responses = [
        item["response"]
        for item in results
        if item.get("source") == "menu"
    ]
    order_responses = [
        item["response"]
        for item in results
        if item.get("source") == "order"
    ]

    # If this turn only needs the menu agent, return its answer directly.
    if menu_responses and not order_responses:
        logger.info("Returning menu response directly.")
        return {"final_answer": menu_responses[-1]}

    # If this turn only needs the order agent, return its answer directly.
    if order_responses and not menu_responses:
        logger.info("Returning order response directly.")
        return {"final_answer": order_responses[-1]}

    # Only combine responses when both agents have responded.
    if menu_responses and order_responses:
        logger.info("Combining menu and order responses.")

        answer = synthesize_response(
            menu_response=menu_responses[-1],
            order_response=order_responses[-1],
        )
        return {"final_answer": answer}

    return {
        "final_answer": (
            "Sorry, I could not process your request. Please try again."
        )
    }
