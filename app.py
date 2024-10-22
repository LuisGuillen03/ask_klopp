import streamlit as st
from prompt_augmentation import generate_augmented_prompt
from clients import openai_client

st.title("Ask Klopp")

st.sidebar.title("Opciones")
context_db = st.sidebar.selectbox(
    "Circulo",
    ["Inversion"]
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    sources , augmented_prompt = generate_augmented_prompt(prompt, context_db.lower())
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = openai_client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]  # Todos menos el último mensaje
            ] + [{"role": "user", "content": augmented_prompt}],  # Añadir el augmented prompt como último mensaje
            stream=True,
        )
        response = st.write_stream(stream)
        # Añadir las fuentes como referencias al final de la respuesta
        references = "\nReferencias:\n" + "\n".join(f"- {source}" for source in sources)
        st.markdown(references)

    # Añadir la respuesta completa del asistente a la sesión
    st.session_state.messages.append({"role": "assistant", "content": response})