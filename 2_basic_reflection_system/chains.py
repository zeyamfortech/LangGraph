from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from HF_LLM_local import llm
from dotenv import load_dotenv

load_dotenv()


llm_gemini = ChatGoogleGenerativeAI(model = "gemini-flash-2.5")
llm_hf = llm

generator_prompt  = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a linkedin techie influencer assistant tasked with writing excellent linkedin posts."
            " Generate the best possible linkedin post for user's request."
            " If the user provide the critiques, respond with the revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name= "messages"),
    ]
)


reflection_prompt  = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            " You are a viral linkedin influencer grading a linkedin posts. Generate the critiques and recommendations for user's post"
            " Always provides detailed recommendations, including requests for length, virality, styles etc.",
        ),
        MessagesPlaceholder(variable_name= "messages"),
    ]
)


generator_chain = generator_prompt | llm_hf
reflection_chain = reflection_prompt | llm_hf

