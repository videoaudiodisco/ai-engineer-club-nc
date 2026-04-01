from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from .state import SocraticState

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """Lazy initialization: Only connects to OpenAI when needed."""
    return ChatOpenAI(model="gpt-4o", temperature=0.2)


def supervisor_node(state: SocraticState):
    """Analyzes the claim and formats the question for the user."""
    # If a path is already selected, we don't need to ask again.
    if state.get("selected_path"):
        return {}

    prompt = (
        f"The user has made the following claim: '{state['claim']}'.\n"
        "Ask the user how they would like to proceed. Provide these exact three options:\n"
        "1. Fact-checking and supporting evidence.\n"
        "2. A Socratic counter-argument to test the logic.\n"
        "3. A review of the historical, ethical, and social implications."
    )
    llm = get_llm()  # Initialize here
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"messages": [response]}


def support_agent_node(state: SocraticState):
    prompt = SystemMessage(
        content="You are a meticulous Fact-Checker. Provide empirical data, "
        "academic consensus, and statistics to support the user's claim."
    )
    llm = get_llm()  # Initialize here
    response = llm.invoke([prompt] + state["messages"])
    return {"messages": [response]}


def socratic_agent_node(state: SocraticState):
    prompt = SystemMessage(
        content="You are a Devil's Advocate. Engage in Socratic questioning. "
        "Identify logical fallacies, edge cases, and counter-evidence "
        "to constructively challenge the user's claim."
    )
    llm = get_llm()  # Initialize here
    response = llm.invoke([prompt] + state["messages"])
    return {"messages": [response]}


def contextual_agent_node(state: SocraticState):
    prompt = SystemMessage(
        content="You are a Contextual Reviewer. Analyze the broader social, "
        "historical, and ethical implications of the user's claim. "
        "Do not strictly support or deny; instead, widen the perspective."
    )
    llm = get_llm()  # Initialize here
    response = llm.invoke([prompt] + state["messages"])
    return {"messages": [response]}
