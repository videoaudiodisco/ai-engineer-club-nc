from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import SocraticState
from .nodes import (
    supervisor_node,
    support_agent_node,
    socratic_agent_node,
    contextual_agent_node,
)


def route_based_on_choice(state: SocraticState):
    """Reads the state and routes to the correct agent."""
    choice = state.get("selected_path")
    if choice == "support":
        return "support_agent"
    elif choice == "socratic":
        return "socratic_agent"
    elif choice == "contextual":
        return "contextual_agent"
    return END  # Fallback


def create_multi_agent_graph():
    workflow = StateGraph(SocraticState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("support_agent", support_agent_node)
    workflow.add_node("socratic_agent", socratic_agent_node)
    workflow.add_node("contextual_agent", contextual_agent_node)

    # FIX 1: Return an empty dict so it doesn't duplicate state
    workflow.add_node("router_node", lambda state: {})

    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", "router_node")

    # FIX 2: Explicitly map the routing paths
    workflow.add_conditional_edges(
        "router_node",
        route_based_on_choice,
        {
            "support_agent": "support_agent",
            "socratic_agent": "socratic_agent",
            "contextual_agent": "contextual_agent",
            END: END,
        },
    )

    workflow.add_edge("support_agent", END)
    workflow.add_edge("socratic_agent", END)
    workflow.add_edge("contextual_agent", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["router_node"])
