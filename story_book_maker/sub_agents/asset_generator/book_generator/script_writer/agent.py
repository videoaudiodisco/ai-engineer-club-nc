from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from story_book_maker.callback import before_model_callback

# Absolute import to prevent ModuleNotFoundError
from story_book_maker.state import PageScriptOutput
from .prompt import SCRIPT_WRITER_DESCRIPTION, SCRIPT_WRITER_PROMPT

# Upgraded to gpt-4o. Mini struggles to output pure Pydantic JSON cleanly.
MODEL = LiteLlm(model="openai/gpt-4o")


script_writer_agent = Agent(
    name="ScriptWriterAgent",
    model=MODEL,
    description=SCRIPT_WRITER_DESCRIPTION,
    instruction=SCRIPT_WRITER_PROMPT,
    # output_schema=PageScriptOutput,  # Keeps your original structure
    # output_key="page_scripts",  # Keeps your original structure
    before_model_callback=before_model_callback,
)
