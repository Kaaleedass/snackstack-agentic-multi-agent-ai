
from SnackStack.agents.orchestrator import route_query

queries = [
    "Show me vegan dishes & Track order ORD-201",
    "Hello, what can you help me with?",
]

for query in queries:
    print(f"\nCustomer: {query}")

    decision = route_query(query)

    print(f"Selected agent: {decision.route}")
    print(f"Reason: {decision.reasoning}")
