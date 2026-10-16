
from SnackStack.config import llm, get_logger

logger = get_logger("synthesizer")


def synthesize_response(
    menu_response: str,
    order_response: str,
) -> str:
    """Combine Menu Agent and Order Agent responses into one answer."""

    logger.info("Combining Menu Agent and Order Agent responses")

    prompt = f"""
You are the SnackStack customer support response synthesizer.

Combine the following two agent responses into ONE clear,
friendly, natural answer for the customer.

Rules:
- Preserve the important information from both responses.
- Avoid unnecessary repetition.
- Do not invent details or change prices or order information.
- Use simple, customer-friendly language.

MENU AGENT RESPONSE:
{menu_response}

ORDER AGENT RESPONSE:
{order_response}

Write the final answer to the customer:
"""

    result = llm.invoke(prompt)

    return result.content
