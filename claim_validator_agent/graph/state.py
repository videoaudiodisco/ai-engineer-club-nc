import operator

from typing import Annotated, TypedDict, List, Union, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field


class SocraticState(TypedDict):
    claim: str
    is_valid: bool
    # Messages list is crucial when using ToolNode to track the conversation flow
    messages: Annotated[List[BaseMessage], operator.add]
    supporting_points: str
    adversarial_critique: str
    final_report: str
    selected_path: str


# 3. Guardrail Schema for Conditional Edge
class ClaimValidation(BaseModel):
    """Plan to determine if the claim is researchable."""

    is_researchable: bool = Field(
        description="Whether the claim is a specific statement that can be analyzed."
    )
    reason: str = Field(description="Brief reason for the decision.")
