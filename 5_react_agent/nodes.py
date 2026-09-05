from react_state import AgentState
from agent_reason_runnabel import react_agent_runnable, tools





def reason_node(state : AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return { "agent_outcome" : agent_outcome}



tool_executor = { tool.name : tool for tool in tools}


def act_node(state: AgentState):
    agent_action = state["agent_outcome"]
    tool = tool_executor[agent_action.tool]
    response = tool.invoke(agent_action.tool_input)
    return {"intermediate_steps" : [(agent_action, str(response))]}
