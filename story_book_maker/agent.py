from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.story_planner.agent import story_planner_agent
from .sub_agents.story_writer.agent import story_writer_agent
from .sub_agents.illustrator.agent import illustrator_agent
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
        AgentTool(agent=story_writer_agent),
        AgentTool(agent=illustrator_agent),
    ],
)

root_agent = master_story_agent
