from dotenv import load_dotenv
import os
import base64

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
    FileSearchTool,
    ImageGenerationTool,
)

client = OpenAI()

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

if "agent" not in st.session_state:
    st.session_state.agent = Agent(
        name="Life Coach Agent",
        instructions="""
        
        You are a life coach assistant agent. You should always be thoughtful and careful about the user's feeeling.
        When the user asks a question or statement, you should always try to understand the user's feeeling and try to help the user.
        Always use encouraging and positive tone.

        You have access to the followign tools:
            - Web Search Tool: Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first. 
            Also, when giving life coaching advice, always search the web about the advice first and then give the advice to the user

            - File Search Tool: Use this tool to access the user's private 'personal_goals.txt' and health records. 
    This is the ONLY source of truth for user progress and exercise history.

            - Image Generation Tool : Use this tool to generate image if the user requests it.

        """,
        tools=[
            WebSearchTool(),
            FileSearchTool(
                vector_store_ids=[
                    VECTOR_STORE_ID,
                ],
                max_num_results=3,
            ),
            ImageGenerationTool(
                # 이러한 툴 설정이 필요하다.
                tool_config={
                    "type": "image_generation",
                    "quality": "high",
                    "output_format": "jpeg",
                    "partial_images": 1,  # 이미지가 천천히 생성되는 것을 보여주는 것
                }
            ),
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
                    elif isinstance(content, list):
                        for part in content:
                            if "image_uri" in part:
                                st.image(part["image_uri"])

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
            elif message_type == "file_search_call":
                with st.chat_message("ai"):
                    st.write("🔍 Searched the files...")
            # 이미지를 채팅창에 그려주기
            elif message_type == "image_generation_call":
                image = base64.b64decode(message["result"])
                with st.chat_message("ai"):
                    st.image(image)


# 이것을 먼저 하고, run_agent를 돌려야 한다. 그래야지 과거 메시지가 나타난다.
asyncio.run(paint_history())


async def run_agent(message):
    with st.chat_message("ai"):

        image_placeholder = st.empty()  # image를 담기 위한 컨테이너 생성
        text_placeholder = st.empty()

        response = ""

        st.session_state["image_interpreter"] = image_placeholder
        st.session_state["text_placeholder"] = text_placeholder

        stream = Runner.run_streamed(
            agent,
            message,
            session=session,
        )
        async for event in stream.stream_events():
            if event.type == "raw_response_event":

                if event.data.type == "response.output_text.delta":
                    response += event.data.delta
                    text_placeholder.write(response.replace("$", r"\$"))

                elif event.data.type == "response.image_generation_call.partial_image":
                    image = base64.b64decode(event.data.partial_image_b64)
                    image_placeholder.image(image)


prompt = st.chat_input(
    "Write a message for your assistant",
    accept_file=True,  # 이러면 채팅창에 파일 업로드 가능
    file_type=[
        "txt",
        "jpg",
        "jpeg",
        "png",
    ],  # 업로드 할 수 있는 파일은 txt 파일로 일단 한정
)

# 처음에는 prompt가 txt 였지만, 파일까지 들어가면 class가 되기 때문에 추가 작업이 필요
if prompt:  # prompt가 있으면

    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳ Uploading file...") as status:
                    uploaded_file = client.files.create(
                        file=(file.name, file.getvalue()),
                        purpose="user_data",
                    )

                    status.update(label="⏳ Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID,
                        file_id=uploaded_file.id,
                    )
                    status.update(label="✅ File uploaded", state="complete")

        elif file.type.startswith("image/"):
            with st.status("⏳ Uploading image...") as status:
                file_bytes = file.getvalue()  # file의 raw data를 가져오기
                base64_data = base64.b64encode(file_bytes).decode("utf-8")  # 인코딩
                data_uri = f"data:{file.type};base64,{base64_data}"  # chatgpt가 인식할 수 있도록 uri 생성
                # 메모리에 이미지를 추가하되, 다만 이것이 일반 텍스트가 아니라 이미지라는 것을 명시해야 함
                asyncio.run(
                    session.add_items(
                        [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "input_image",
                                        "detail": "auto",
                                        "image_url": data_uri,
                                    }
                                ],
                            }
                        ]
                    )
                )
                status.update(label="✅ Image uploaded", state="complete")

            # 이미지 업로드하고 이미지를 채팅창에 보여주기
            with st.chat_message("human"):
                st.image(data_uri)

    # 파일을 먼저 처리해야지, 안그러면 파일과 관련된 질문을 하면 chatgpt가 모른다.
    if prompt.text:
        with st.chat_message("human"):
            st.write(prompt.text)
        asyncio.run(run_agent(prompt.text))


with st.sidebar:
    reset = st.button("Reset Memory")
    if reset:  # reset button을 누르면 true가 된다.
        asyncio.run(session.clear_session())
    # sidebar에 대화 기록 전체를 표시
    st.write(asyncio.run(session.get_items()))
