from typing import List
from langchain_core.messages import BaseMessage, ToolMessage, Human
from langgraph.graph import END, MessageGraph
from chains import reviser_chain, first_responder_chain
from execute_tools import execute_tool


graph = MessageGraph()
Max_iterations = 2


graph.add_node("draft", first_responder_chain)
graph.add_node("execute_tools", execute_tool)
graph.add_node("revisor", reviser_chain)



graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor")

def event_loop(state : List[BaseMessage]) -> str:
    count_tool_visits = sum((isinstance(item, ToolMessage)) for item in state)

    if count_tool_visits > Max_iterations:
        return END
    else:
        return execute_tool
    

graph.add_conditional_edges("revisor", event_loop)
graph.set_entry_point("draft")


app = graph.compile()

print(app.get_graph().draw_mermaid())

response = app.invoke("write about how small businesses can leverage AI to grow")


print(response)

print(response[-1].tool_calls[0]["args"]["answer"])