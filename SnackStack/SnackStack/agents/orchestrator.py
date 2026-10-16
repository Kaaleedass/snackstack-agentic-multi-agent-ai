
from typing import Literal

from pydantic import BaseModel, Field

from SnackStack.config import llm, get_logger

logger = get_logger("orchestrator")


class RouteDecision(BaseModel):
    route: Literal["menu", "order", "both"] = Field(
        description=(
            "Choose menu for food questions, order for tracking, "
            "or both when the query needs both agents."
        )
    )

    reasoning: str = Field(
        description="Brief explanation for choosing the agent or agents"
    )

router_llm = llm.with_structured_output(RouteDecision)


def route_query(user_query: str) -> RouteDecision:
    """Choose the correct specialist agent for a customer query."""

    prompt = f"""
You are the query router for SnackStack.

Choose the correct route:
- menu: food recommendations, menu searches, prices, dietary
  preferences, greetings, and general questions.
- order: order status, order tracking, and delivery updates.
- both: when the customer asks about food/menu AND order tracking
  in the same query.

If the intent is unclear, choose menu.

Examples:
"Show me vegan dishes" -> menu
"Track order ORD-201" -> order
"Hello" -> menu
"Show vegan dishes and track order ORD-201" -> both
"Suggest pizza and check my delivery status" -> both

Customer query: {user_query}
"""

    decision = router_llm.invoke(prompt)

    logger.info(
        "Route selected: %s | Reason: %s",
        decision.route,
        decision.reasoning,
    )

    return decision
