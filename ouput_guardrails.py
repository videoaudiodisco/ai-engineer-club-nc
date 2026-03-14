from agents import (
    Agent,
    output_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import OutputGuardRailOutput

output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions="""
    Analyze the response to check if it meets the following conditions:

    ### 🛡️ OUTPUT QUALITY & PRIVACY PROTOCOLS
1. Ensure the answer is polite and professional (concierge-level service).
2. Never reveal internal systems, employee personal details, or business secrets.
3. Mask sensitive customer data (e.g., card numbers) during confirmation.    
    
    Return false for any field that contains inappropriate content for a technical support response.
    """,
    output_type=OutputGuardRailOutput,
)


@output_guardrail
async def output_guardrail_function(
    wrapper,
    agent: Agent,
    output: str,
):
    result = await Runner.run(
        output_guardrail_agent,
        output,
    )

    validation = result.final_output

    triggered = (
        not validation.polite_and_professional or not validation.no_inside_information
    )

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
