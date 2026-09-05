from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, add_messages
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

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


# memory = MemorySaver()# in memory checkpoint saver, when we stop/end the prohgram it will no longer remember the previous conversation

db_connection = sqlite3.connect("checkpoints.sqlite", check_same_thread = False)# using external db for storing states even programme is ended still remember the conversation 
memory = SqliteSaver(db_connection)


app = graph.compile(checkpointer = memory)
config = {
    "configurable":{
        "thread_id": 1
    }
}


while True:
    user_input = input("User input: ")

    if user_input.lower() in ["end", "exit"]:
        break
    else:
        result = app.invoke({
                "messages": [HumanMessage(content=user_input)]
        }, config=config)
        print(result['messages'][-1].content)