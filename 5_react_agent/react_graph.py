from nodes import reason_node, act_node
from react_state import AgentState
from langgraph.graph import StateGraph, END
from langchain_core.agents import AgentAction, AgentFinish
from dotenv import load_dotenv

load_dotenv()



REASON_NODE = "reason_node"
ACT_NODE = "act_node"


def should_continue(state: AgentState):
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT_NODE
    

work_flow = StateGraph(AgentState)


work_flow.add_node(REASON_NODE, reason_node)
work_flow.set_entry_point(REASON_NODE)
work_flow.add_node(ACT_NODE, act_node)
work_flow.add_conditional_edges(REASON_NODE, should_continue)
work_flow.add_edge(ACT_NODE, REASON_NODE)


app = work_flow.compile()

result = app.invoke(
    {
    "input": "How many days ago was the latest SpacsX launch ", 
    "agent_outcome": None,
    "intermediate_steps": []
    }
)

print(result)
# print(result["agent_outcome"].return_values["output"], "final_result")