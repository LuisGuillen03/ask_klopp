import time
import streamlit as st
import google.generativeai as genai
from prompt_augmentation import generate_augmented_prompt
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'


st.write('# Ask Klopp')

# Chat history (allows to ask multiple questions)
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    st.session_state.model = genai.GenerativeModel('gemini-1.5-pro-latest')
    st.session_state.chat = st.session_state.model.start_chat(
        history=st.session_state.gemini_history,
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Ask Klopp...'):
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    ## Send message to AI
    prompt_with_context = generate_augmented_prompt(prompt)
    print(prompt_with_context)
    response = st.session_state.chat.send_message(
        prompt_with_context,
        stream=True,
    )
    # Display assistant response in chat message container
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                # Rewrites with a cursor at end
                message_placeholder.write(full_response + '▌')
        # Write full message with placeholder
        message_placeholder.write(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history