from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field
from typing import List
from .prompt import STORY_WRITER_DESCRIPTION, STORY_WRITER_PROMPT


# Define the structured output
class PageDef(BaseModel):
    page_number: int
    text: str
    visual_description: str


class StoryBookOutput(BaseModel):
    pages: List[PageDef]


MODEL = LiteLlm(model="openai/gpt-4o")

story_writer_agent = Agent(
    name="StoryWriterAgent",
    model=MODEL,
    description=STORY_WRITER_DESCRIPTION,
    instruction=STORY_WRITER_PROMPT,
    output_schema=StoryBookOutput,  # Forces LLM to output this JSON structure
    output_key="story_book_draft",  # Saves the JSON directly to the shared State under this key
)
