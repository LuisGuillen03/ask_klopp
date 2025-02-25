import streamlit as st
import requests

st.title("Ask Klopp")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "USER", "content": prompt})
    with st.chat_message("USER"):
        st.markdown(prompt)

    with st.chat_message("ASSISTANT"):
        # Preparar payload para la API
        payload = {"messages": [{"role": "USER", "content": prompt}]}
        headers = {"KloppChat-API-Key": "KLOPP_CHAT_API_KEY"}
        
        # Llamada a la API
        response = requests.get(st.secrets["KLOPP_CHAT_URL"], json=payload, headers=headers)
        data = response.json()
        
        # Extraer el contenido de la respuesta
        answer = data.get("content", "")
        st.markdown(answer)
        
        # Extraer la URL de los videos (fuentes)
        sources = []
        media = data.get("media", {})
        for video in media.get("videos", []):
            url = video.get("url")
            if url:
                sources.append(url)
        
        if sources:
            references = "\nReferencias:\n" + "\n".join(f"- {source}" for source in sources)
            st.markdown(references)
    
    # Agregar la respuesta del asistente al historial de mensajes
    st.session_state.messages.append({"role": "ASSISTANT", "content": answer})