from langchain_google_genai import ChatGoogleGenerativeAI
from chains import generator_chain, reflection_chain
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph


load_dotenv()


graph = MessageGraph()


REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state):
    return generator_chain.invoke(
        {
            "messages": state
        }
    )


def reflect_node(state):
    response = reflection_chain.invoke(
        {
        "messages": state
        }
    )
    return [HumanMessage(content = response)]


def should_continue(state):
    if len(state)>2:
        return END
    else:
        return REFLECT   
    

graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)

graph.set_entry_point(GENERATE)

graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)


app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()



response = app.invoke(HumanMessage(content = "AI Agents taking over the content creation"))

print(response)