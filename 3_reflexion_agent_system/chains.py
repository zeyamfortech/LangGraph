from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import datetime
from schemas import AnswerQuestion, RevisedAnswer
from dotenv import load_dotenv


load_dotenv()


# LLM

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

# Pydantic Parser

pydantic_parser = PydanticOutputParser(pydantic_object = AnswerQuestion)




# Actor agent prompt
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ you are expert AI researcher.
            
            current time : {time}
            
            1. {first_instruction}
            2. reflect and critique your answer. be sever to maximize improvement.
            3. After the reflection, list 1-3 search queries separately for researching improvements.
            Do not include them inside the reflection.
            """,
            ),
            MessagesPlaceholder(variable_name= "messages"),
            ("system", "Answer the user question above using the required formate."),      
        
    ]
).partial(
    time = lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = "Provide a detailed ~250 words answer"
)


revisor_instruction = """ Revise your previous answer using the new information.
   - you should use the previous critique to add important information to your answer.
   - you must include numerical citations in your revised answer to ensure it can be verified.
   - Add references section to the bottom to your answer (which does not count towards the word limit). in the form of :
        - [1] https://example.com
        - [2] https://example.com

   - you should use the previous critique to remove the superfluous information from your answer and make sure it is not more than 250 words  
"""

reviser_prompt_template = actor_prompt_template.partial(
    first_instruction = revisor_instruction
)


reviser_chain = reviser_prompt_template | llm.bind_tools(tools=[RevisedAnswer], tool_choice="RevisedAnswer")




# Chain(for gemini-2.5-flash we don't apply the parser other models might expect)

first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")


response = first_responder_chain.invoke({
    "messages": [HumanMessage(content = "write me a blog post on how small bussinesses can leverage AI to grow" )]
})
 
print(response)



