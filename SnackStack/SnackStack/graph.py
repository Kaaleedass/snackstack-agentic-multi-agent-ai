
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from SnackStack.state import StackState
from SnackStack.nodes import (
    orchestrator_node,
    menu_node,
    order_node,
    synthesizer_node,
)

builder = StateGraph(StackState)

# Register the four main nodes
builder.add_node("orchestrator", orchestrator_node)
builder.add_node("menu_agent", menu_node)
builder.add_node("order_agent", order_node)
builder.add_node("synthesizer", synthesizer_node)

# Entry and exit
builder.add_edge(START, "orchestrator")
builder.add_edge("synthesizer", END)

# Compile
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
