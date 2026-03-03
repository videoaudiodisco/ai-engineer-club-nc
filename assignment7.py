from dotenv import load_dotenv

load_dotenv()

import dotenv
from openai import OpenAI

import asyncio
import streamlit as st
from agents import (
    Agent,
    Runner,
    SQLiteSession,
    WebSearchTool,
)

if "agent" not in st.session_state:
    st.session_state.agent = Agent(
        name="Life Coach Agent",
        instructions="""
        
        You are a life coach assistant agent. You should always be thoughtful and careful about the user's feeeling.
        When the user asks a question or statement, you should always try to understand the user's feeeling and try to help the user.
        Always use encouraging and positive tone.

        You have access to the followign tools:
            - Web Search Tool: Use this when the user asks a questions that isn't in your training data. 
            Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first. 
            Also, when giving life coaching advice, search the web about the advice first and then give the advice to the user
        """,
        tools=[
            WebSearchTool(),
        ],
    )


agent = st.session_state.agent

if "session" not in st.session_state:
    st.session_state.session = SQLiteSession(
        "chat-history",  # session id
        "life-coach-advice.db",  # db path and name
    )

# session을 앞으로도 사용해야 하므로, 사용하기 편하게 이렇게 빼줌
session = st.session_state.session


# session 에 있는 과거 메시지를 메인 화면에 표시
async def paint_history():

    messages = await session.get_items()

    for message in messages:
        # role 이 있으면
        if "role" in message:
            # 메인 채팅창 화면에 표시
            with st.chat_message(message["role"]):
                # user message 이면 그것을 표시
                if message["role"] == "user":
                    # content의 종류에 따라 채팅창에 다르게 표시
                    content = message["content"]
                    if isinstance(content, str):
                        st.write(content)

                # user가 아니라면 ai 가 만든 메시지
                else:
                    if message["type"] == "messasge":  # 나중에 tool 등 때문에?
                        st.write(
                            message["content"][0]["text"].replace("$", r"\$")
                        )  # ai 메시지의 text를 표시

        # tool 사용시, 일종의 tool_call 처럼 아예 role 이 없고 type만 있는 경우가 생긴다.
        if "type" in message:
            message_type = message["type"]
            if message_type == "web_search_call":
                with st.chat_message("ai"):
                    st.write("🔍 Searched the web...")


# 이것을 먼저 하고, run_agent를 돌려야 한다. 그래야지 과거 메시지가 나타난다.
asyncio.run(paint_history())


async def run_agent(message):
    with st.chat_message("ai"):

        text_placeholder = st.empty()  # ai message를 담기 위해서 빈 컨테이너를 생성.
        response = ""
        stream = Runner.run_streamed(
            agent,
            message,
            session=session,
        )
        async for event in stream.stream_events():
            if event.type == "raw_response_event":

                # 이렇게 하면 글씨가 조금씩 써지는 것이 보인다.
                if event.data.type == "response.output_text.delta":
                    response += event.data.delta
                    text_placeholder.write(response.replace("$", r"\$"))


prompt = st.chat_input(
    "Write a message for your life coach agent",
)

if prompt:  # prompt가 있으면
    with st.chat_message("human"):
        st.write(prompt)
    asyncio.run(run_agent(prompt))

with st.sidebar:
    reset = st.button("Reset Memory")
    if reset:  # reset button을 누르면 true가 된다.
        asyncio.run(session.clear_session())
    # sidebar에 대화 기록 전체를 표시
    st.write(asyncio.run(session.get_items()))
