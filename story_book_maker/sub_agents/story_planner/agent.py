from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import STORY_PLANNER_DESCRIPTION, STORY_PLANNER_PROMPT
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")

story_planner_agent = Agent(
    name="StoryPlannerAgent",
    model=MODEL,
    description=STORY_PLANNER_DESCRIPTION,
    instruction=STORY_PLANNER_PROMPT,
    # No tools needed for this agent as it is a pure reasoning node
)
