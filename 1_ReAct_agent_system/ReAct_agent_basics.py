from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent
from langchain_community.tools import TavilySearchResults, tool
from dotenv import load_dotenv
import datetime


load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
search_tool = TavilySearchResults(search_depth = "basic")

@tool
def get_system_time(format :str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system date and time in the specified format."""

    current_date = datetime.datetime.now()
    formated_date_time = current_date.strftime(format)
    return formated_date_time    



tools = [search_tool, get_system_time] 

agent = initialize_agent(llm=llm, tools=tools, agent="zero-shot-react-description", handle_parsing_errors=True, verbose = True)

# result = llm.invoke("what is the weather conditions in the Gujranwala Pakistan today")
# print(result)

agent.invoke("what was the last launch date of SpaceX and how many days ago from today")


