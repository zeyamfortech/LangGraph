from langgraph.graph import StateGraph, END
from typing import TypedDict


class SimpleState(TypedDict):
    count : int
    



def increment(state: SimpleState) -> SimpleState:
    return{
        "count": state["count"] + 1
    }


def should_continue(state):
    if state["count"] < 5:
        return "increment"
    else:
        return END
    


graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment", should_continue)

app = graph.compile()

initial_state = {
    "count" : 0
    }

response = app.invoke(
        initial_state
        )

print(response)