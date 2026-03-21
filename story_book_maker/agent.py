from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.story_planner.agent import story_planner_agent
from .sub_agents.asset_generator.agent import asset_generator_agent
from .prompt import MASTER_DESCRIPTION, MASTER_PROMPT

from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")


master_story_agent = Agent(
    name="MasterStoryAgent",
    model=MODEL,
    description=MASTER_DESCRIPTION,
    instruction=MASTER_PROMPT,
    tools=[
        AgentTool(agent=story_planner_agent),
        AgentTool(agent=asset_generator_agent),
    ],
)

root_agent = master_story_agent
