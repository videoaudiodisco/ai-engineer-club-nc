from google.adk.agents import SequentialAgent
from .story_writer.agent import story_writer_agent
from .book_generator.agent import book_generator_agent
from .prompt import ASSET_GENERATOR_DESCRIPTION


asset_generator_agent = SequentialAgent(
    name="AssetGeneratorAgent",
    description=ASSET_GENERATOR_DESCRIPTION,
    sub_agents=[
        story_writer_agent,
        book_generator_agent,
    ],
)
