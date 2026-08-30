from pydantic import BaseModel, Field
from HF_LLM_local import chats
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

class Country(BaseModel):
    "information about any country"

    name: str = Field(description="name of the coutry")
    language: str = Field(description="language speak in that country")
    capital: str = Field(description="Capital city name of that country")



structured_llm = llm.with_structured_output(Country)

rersult = structured_llm.invoke("tell us about the Pakistan")

print(rersult)

