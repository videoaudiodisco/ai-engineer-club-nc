import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from claim_validator_agent.graph.builder import create_multi_agent_graph

st.set_page_config(page_title="Multi-Agent Synthesizer", layout="centered")


# --- 1. STREAMLIT CALLBACKS (THE FIX) ---
# These run BEFORE the rest of the page loads, guaranteeing a clean state.
def reset_analysis():
    """Wipes the text box, unlocks it, and resets the AI memory."""
    st.session_state.claim_submitted = False
    st.session_state.claim_input_widget = ""  # This explicitly clears the text box
    st.session_state.thread_id = str(
        uuid.uuid4()
    )  # Gives LangGraph a fresh memory thread


def mark_submitted():
    """Locks the text box and triggers the AI."""
    if st.session_state.claim_input_widget.strip():
        st.session_state.claim_submitted = True


# --- 2. INITIALIZATION ---
if "agent" not in st.session_state:
    st.session_state.agent = create_multi_agent_graph()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.claim_submitted = False
    st.session_state.claim_input_widget = ""  # Tie the widget to session state

config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("Socratic Synthesizer")

# --- 3. UI INPUT ---
# By setting key="claim_input_widget", we can control the text directly from the callback.
st.text_input(
    "Enter your claim:",
    key="claim_input_widget",
    disabled=st.session_state.claim_submitted,
    on_change=mark_submitted,  # Allows hitting "Enter" to submit
)

st.button(
    "Submit Claim", on_click=mark_submitted, disabled=st.session_state.claim_submitted
)

# --- 4. GRAPH EXECUTION ---
if st.session_state.claim_submitted:
    current_state = st.session_state.agent.get_state(config)

    # Check if the graph hasn't started yet for this thread
    if not current_state.values:
        with st.spinner("Supervisor is reviewing the claim..."):
            initial_state = {
                "claim": st.session_state.claim_input_widget,
                "messages": [HumanMessage(content=st.session_state.claim_input_widget)],
            }
            st.session_state.agent.invoke(initial_state, config)
        st.rerun()

    # Get updated state after the initial run
    current_state = st.session_state.agent.get_state(config)

    # If paused at the router, ask the user for their choice
    if current_state.next == ("router_node",):
        last_message = current_state.values["messages"][-1].content
        st.info(f"**Supervisor:** {last_message}")

        st.write("### How would you like to proceed?")
        col1, col2, col3 = st.columns(3)

        chosen_path = None
        if col1.button("1. Fact Check"):
            chosen_path = "support"
        if col2.button("2. Socratic Critique"):
            chosen_path = "socratic"
        if col3.button("3. Contextual Review"):
            chosen_path = "contextual"

        if chosen_path:
            # Update LangGraph state with human choice
            st.session_state.agent.update_state(
                config,
                {
                    "selected_path": chosen_path,
                    "messages": [HumanMessage(content=f"I choose path {chosen_path}")],
                },
                as_node="supervisor",
            )

            # Resume execution
            with st.spinner("Agent is analyzing... (This may take a moment)"):
                st.session_state.agent.invoke(None, config)
            st.rerun()  # Rerun to display the final output cleanly

    # If graph is fully finished (no next node)
    elif not current_state.next and current_state.values:
        st.success("Analysis Complete!")
        st.markdown(current_state.values["messages"][-1].content)

        # --- 5. RESET BUTTON ---
        # Using on_click triggers the reset_analysis function at the very top of the script
        st.button("Start New Analysis", on_click=reset_analysis)
