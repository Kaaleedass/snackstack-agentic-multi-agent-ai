
"""
Order Search Tool for SnackStack.
Finds orders using order ID, tracking ID, or email.
"""

import re

from langchain.tools import tool

from SnackStack.config import get_logger
from SnackStack.data.orders import orders_db

logger = get_logger("order_tools")


@tool
def get_order_status(identifier: str) -> str:
    """
    Find a SnackStack order by order ID, tracking ID, or customer email.

    Args:
        identifier: An order ID such as ORD-201,
                    tracking ID such as SS201TRK,
                    or customer email address.
    """
    identifier = identifier.strip()

    # Extract an order ID, tracking ID, or email from the input.
    order_match = re.search(
        r"\bORD-\d+\b", identifier, re.IGNORECASE
    )
    tracking_match = re.search(
        r"\bSS\d+TRK\b", identifier, re.IGNORECASE
    )
    email_match = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", identifier
    )

    search_value = (
        order_match.group(0).upper() if order_match
        else tracking_match.group(0).upper() if tracking_match
        else email_match.group(0).lower() if email_match
        else identifier
    )

    for order in orders_db.values():
        if (
            order["order_id"].upper() == search_value.upper()
            or order["tracking_id"].upper() == search_value.upper()
            or order["customer_email"].lower() == search_value.lower()
        ):
            logger.info("Order found: %s", order["order_id"])

            return (
                f"Order ID: {order['order_id']}\n"
                f"Item: {order['item_name']}\n"
                f"Customer: {order['customer_name']}\n"
                f"Status: {order['status']}\n"
                f"Tracking ID: {order['tracking_id']}\n"
                f"Email: {order['customer_email']}"
            )

    logger.info("No order found for: %s", search_value)
    return f"No order found for: {search_value}"
