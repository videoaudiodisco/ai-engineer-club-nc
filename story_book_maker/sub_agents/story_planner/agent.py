from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from .prompt import STORY_PLANNER_DESCRIPTION, STORY_PLANNER_PROMPT
from google.adk.models.lite_llm import LiteLlm
from story_book_maker.callback import before_model_callback

MODEL = LiteLlm(model="openai/gpt-4o")

story_planner_agent = Agent(
    name="StoryPlannerAgent",
    model=MODEL,
    description=STORY_PLANNER_DESCRIPTION,
    instruction=STORY_PLANNER_PROMPT,
    before_model_callback=before_model_callback,
)
