from pydantic import BaseModel
from typing import Optional


class HandoffData(BaseModel):
    to_agent_name: str
    customer_request: str
    reason: str


class InputGuardRailOutput(BaseModel):

    input_guardrail_on: bool  # if question is off topic or use inappropriate language
    reason: str


class OutputGuardRailOutput(BaseModel):

    polite_and_professional: bool
    no_inside_information: bool
    reason: str
