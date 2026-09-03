from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator


class SimpleState(TypedDict):
    count : int
    sum : Annotated[int, operator.add] # data type plus what it does actually
    history: Annotated[List[int], operator.concat] # data type plus what it does actually


def increment(state: SimpleState) -> SimpleState:

    latest_count = state["count"] + 1

    return{
        "count":latest_count,
        "sum": latest_count,
        "history": [latest_count]
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
    "count" : 0,
    "sum" : 0,
    "history" : [] 
    }

response = app.invoke(
        initial_state
        )

print(response)