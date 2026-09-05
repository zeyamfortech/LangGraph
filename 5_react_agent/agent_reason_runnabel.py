from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, create_react_agent
from langchain_community.tools import TavilySearchResults
import datetime
from langchain import hub
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()



llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

search_tool = TavilySearchResults(search_depth = "basic")


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Return the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formated_time = current_time.strftime(format)
    return formated_time


tools = [search_tool, get_system_time]


react_prompt = PromptTemplate.from_template(
"""
Answer the following questions as best you can.

You have access to the following tools:

{tools}

Use the following format:

Question: {input}

Thought: think about what to do

Action: one of [{tool_names}]

Action Input: input to the action

Observation: result of the action

...(repeat Thought/Action/Observation)...

Thought: I now know the final answer

Final Answer: the answer to the original question

Question: {input}

{agent_scratchpad}
"""
)

react_agent_runnable = create_react_agent(llm = llm, tools = tools, prompt = react_prompt)

