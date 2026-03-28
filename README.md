## Socratic Synthesizer: Deep Research & Critical Thinking Agent

This project implements a multi-agent system designed to analyze claims through a rigorous Socratic lens. It moves beyond simple prompt-response cycles by employing an adversarial architecture that supports, challenges, and finally synthesizes information to provide a balanced, high-depth analysis report.

### 🏗 Architecture & Workflow

The system is built using **LangGraph**, enabling a stateful, cyclic directed acyclic graph (DAG) that manages the flow of information between specialized nodes.

1.  **Validator Node (Conditional Gatekeeper)**:
    - Uses structured output to assess if the user's input is a researchable claim.
    - **Conditional Edge**: If the claim is valid, it proceeds to research; otherwise, it terminates early to save tokens and latency.
2.  **Research Node (Support)**:
    - Integrated with the **Tavily Search Tool** to gather real-time, evidence-based data.
    - Constructs the strongest possible defense for the claim using logical frameworks.
3.  **Socratic Node (Adversarial)**:
    - Acts as the "Devil's Advocate".
    - Scrutinizes the research for logical fallacies, identifies blind spots, and presents strong counter-arguments.
4.  **Synthesis Node (Moderator)**:
    - Integrates both the defense and the critique.
    - Produces a final "State of the Debate" report featuring an executive summary and a nuanced middle-ground perspective.

---

### 🚀 Key Features

- **Real-world Grounding**: Leverages Tavily Search to prevent model hallucinations and ensure data is current.
- **State Management**: Utilizes `TypedDict` and `operator.add` to maintain a robust record of the reasoning process and message history.
- **Production-Ready Logic**: Includes a validation step to handle nonsensical inputs and uses high-reasoning models (GPT-4o) for complex synthesis.
- **Type Safety**: Employs Pydantic schemas for structured LLM outputs, ensuring reliable routing within the graph.

### 🛠 Tech Stack

- **Orchestration**: LangGraph
- **LLM**: OpenAI GPT-4o
- **Tools**: Tavily Search API
- **Language**: Python 3.10+

---

### 📋 Prerequisites

```bash
pip install langgraph langchain_openai langchain_community tavily-python
```

### 🚦 Quick Start

1. Set your environment variables:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   export TAVILY_API_KEY='your-tavily-key'
   ```
2. Run the graph:

   ```python
   # Initialize the state
   initial_state = {"user_claim": "Universal Basic Income is necessary due to AI automation."}

   # Execute the workflow
   final_output = app.invoke(initial_state)
   print(final_output['final_report'])
   ```

Would you like me to add a **human-in-the-loop** interruption after the Socratic critique so you can provide your own feedback before the final synthesis?
