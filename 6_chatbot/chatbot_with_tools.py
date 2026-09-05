from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")



search_tool = TavilySearchResults(max_results = 2)
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools=tools)


class ChatbotWithTool(TypedDict):
    messages: Annotated[list, add_messages]


def Chatbot(state: ChatbotWithTool):
    return{
        "messages": [llm_with_tools.invoke(state['messages'])]
    }


def tool_router(state: ChatbotWithTool):

    last_message = state["messages"][-1]
    if (hasattr(last_message, "tool_calls") and (len(last_message.tool_calls) > 0)):
        return "tool_node"
    else:
        return END
    
tool_node = ToolNode(tools=tools) # it automatically knows where to look at messages


graph = StateGraph(ChatbotWithTool)

graph.add_node("chatbot", Chatbot)
graph.add_node("tool_node", tool_node)
graph.add_edge("tool_node", "chatbot")
graph.add_conditional_edges("chatbot", tool_router)
graph.set_entry_point("chatbot")

app = graph.compile()
 

while True:
    user_input = input("User input : ")

    if user_input.lower() in ["end", "exit"]:
        break

    else:
        results = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        print(results["messages"][-1].content)
        print(results)