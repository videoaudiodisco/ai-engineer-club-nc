from google.adk.agents import ParallelAgent
from .illustrator.agent import illustrator_agent as image_generator_agent
from .script_writer.agent import script_writer_agent
from .prompt import BOOK_GENERATOR_AGENT_DESCRIPTION


book_generator_agent = ParallelAgent(
    name="BookGeneratorAgent",
    description=BOOK_GENERATOR_AGENT_DESCRIPTION,
    sub_agents=[
        image_generator_agent,
        script_writer_agent,
    ],
)
