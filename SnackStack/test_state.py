
from SnackStack.state import StackState

state: StackState = {
    "user_query": "Show vegan dishes and track ORD-201",
    "route": "both",
    "menu_response": "Vegan dishes found.",
    "order_response": "ORD-201 is out for delivery.",
}

print("User query:", state["user_query"])
print("Route:", state["route"])
print("Menu response:", state["menu_response"])
print("Order response:", state["order_response"])
