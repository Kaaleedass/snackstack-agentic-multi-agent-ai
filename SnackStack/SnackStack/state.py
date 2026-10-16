
import operator
from typing import Annotated, Literal
from typing_extensions import TypedDict


class StackState(TypedDict, total=False):
    user_query: str
    route: Literal["menu", "order", "both"]
    reasoning: str

    # Each agent contributes its own result.
    agent_results: Annotated[list[dict], operator.add]

    final_answer: str
