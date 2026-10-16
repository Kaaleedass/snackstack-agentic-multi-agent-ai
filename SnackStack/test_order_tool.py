
from SnackStack.Tools.order_tools import get_order_status

# Test 1: Search by Order ID
print("\n--- TEST 1: ORDER ID ---")
print(get_order_status.invoke({"identifier": "ORD-201"}))

# Test 2: Search by Tracking ID
print("\n--- TEST 2: TRACKING ID ---")
print(get_order_status.invoke({"identifier": "SS202TRK"}))

# Test 3: Search by Email
print("\n--- TEST 3: EMAIL ---")
print(
    get_order_status.invoke({
        "identifier": "priya@example.com"
    })
)

# Test 4: Unknown order
print("\n--- TEST 4: UNKNOWN ORDER ---")
print(
    get_order_status.invoke({
        "identifier": "ORD-999"
    })
)
