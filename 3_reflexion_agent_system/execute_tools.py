import json
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_community.tools import TavilySearchResults

# Create the tavilyb search tool
tavily_tool = TavilySearchResults(max_results = 5)


# Function to execute the search quries fropm AnswerQuestion toll calls

def execute_tool(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message : AIMessage = state[-1]


    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        return []
    
    # process the AnswerQuestion or RevisedAnswer toll calls to extract search queries
    tool_messages = []
 
    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "RevisedAnswer"]:
            call_id = tool_call['id']
            searh_queries = tool_call['args'].get("search_queries", [])

            # Execute the each search using the tavily search tool

            query_results = {}
            for query in searh_queries:
                result = tavily_tool.invoke(query)
                query_results["query"] = result

            # Create a tool meassage 

            tool_messages.append(
                ToolMessage(
                    content = json.dumps(query_results),
                    tool_call_id = call_id
                )
            )

    return tool_messages            