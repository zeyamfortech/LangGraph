from pydantic import BaseModel, Field
from typing import List, Optional

class Reflection(BaseModel):
    missing : str = Field(description="Critique of what is missing")
    superfluous : str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    answer : str = Field(description="~250 words detailed answer of question.")
    search_queries : List[str] = Field(description="1-3 search queries for researching improvements to address the critique of your answer.")
    reflection : Reflection = Field(description="your reflection on the initial answer")


class RevisedAnswer(AnswerQuestion):
    """ revise your original answer to your question """

    references : List[str] = Field(description="Citations motivating your updated answer.")