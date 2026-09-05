from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]


def Chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state['messages'])]
    }


graph = StateGraph(BasicChatState)

graph.add_node("chatbot", Chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()


while True:
    user_input = input("User input: ")

    if user_input.lower() in ["end", "exit"]:
        break
    else:
        result = app.invoke({
                "messages": [HumanMessage(content=user_input)]
        })
        print(result)