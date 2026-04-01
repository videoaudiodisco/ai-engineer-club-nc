import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from graph.builder import create_multi_agent_graph
import traceback

try:
    st.set_page_config(page_title="Claim Validator", layout="centered")

    def reset_analysis():
        st.session_state.claim_submitted = False
        st.session_state.claim_input_widget = ""
        st.session_state.thread_id = str(uuid.uuid4())

    def mark_submitted():
        if st.session_state.claim_input_widget.strip():
            st.session_state.claim_submitted = True

    if "agent" not in st.session_state:
        st.session_state.agent = create_multi_agent_graph()
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.claim_submitted = False
        st.session_state.claim_input_widget = ""

    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    st.title("⚖️ Claim Validator")

    # --- NEW: User Explanation ---
    with st.expander(
        "ℹ️ How to use this tool", expanded=not st.session_state.claim_submitted
    ):
        st.markdown(
            """
        **Objective:** Analyze any claim using three distinct analytical lenses.
        1. **Enter a claim** (e.g., "Remote work increases long-term productivity").
        2. **Select a Path:** Once the Supervisor reviews your claim, choose whether you want:
            * **Fact Check:** Hard data and evidence.
            * **Socratic Critique:** A logical challenge to your premise.
            * **Contextual Review:** Broad social and ethical implications.
        """
        )

    st.text_input(
        "Enter your claim for analysis:",
        key="claim_input_widget",
        disabled=st.session_state.claim_submitted,
        on_change=mark_submitted,
    )

    if not st.session_state.claim_submitted:
        st.button("Analyze Claim", on_click=mark_submitted)

    if st.session_state.claim_submitted:
        try:
            current_state = st.session_state.agent.get_state(config)

            if not current_state.values:
                with st.spinner("Supervisor is reviewing the claim..."):
                    initial_state = {
                        "claim": st.session_state.claim_input_widget,
                        "messages": [
                            HumanMessage(content=st.session_state.claim_input_widget)
                        ],
                    }
                    st.session_state.agent.invoke(initial_state, config)
                st.rerun()

            current_state = st.session_state.agent.get_state(config)

            if current_state.next == ("router_node",):
                last_message = current_state.values["messages"][-1].content
                st.info(f"**Supervisor:** {last_message}")

                st.write("### Choose your analytical lens:")
                col1, col2, col3 = st.columns(3)

                chosen_path = None
                if col1.button("📊 Fact Check"):
                    chosen_path = "support"
                if col2.button("🧐 Socratic"):
                    chosen_path = "socratic"
                if col3.button("🌍 Contextual"):
                    chosen_path = "contextual"

                if chosen_path:
                    st.session_state.agent.update_state(
                        config,
                        {
                            "selected_path": chosen_path,
                            "messages": [
                                HumanMessage(content=f"I choose path {chosen_path}")
                            ],
                        },
                        as_node="supervisor",
                    )
                    with st.spinner("Agent is performing deep analysis..."):
                        st.session_state.agent.invoke(None, config)
                    st.rerun()

            elif not current_state.next and current_state.values:
                st.success("Analysis Complete!")
                st.markdown(current_state.values["messages"][-1].content)
                st.button("Start New Analysis", on_click=reset_analysis)

        except Exception as e:
            st.error(f"⚠️ An error occurred during the graph execution.")
            with st.expander("Technical Details"):
                st.code(str(e))
            if st.button("Retry"):
                st.rerun()

except Exception as e:
    st.error("The application encountered a critical startup error.")
    st.code(traceback.format_exc())
