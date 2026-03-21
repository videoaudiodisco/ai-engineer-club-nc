from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest


def before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
):

    print(f"{callback_context.agent_name} is working now....")
