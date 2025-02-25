import streamlit as st
import requests
import vimeo

def vimeo_authentication():
    client = vimeo.VimeoClient(
        token=st.secrets['VIMEO_TOKEN'],
        key=st.secrets['VIMEO_KEY'],
        secret=st.secrets['VIMEO_SECRET']
    )
    return client

vimeo_client = vimeo_authentication()

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
        headers = {"KloppChat-API-Key": st.secrets["KLOPP_CHAT_API_KEY"]}
        
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
            st.markdown("\nReferencias:\n\n")
            for url in sources:
                video_id = url.split("/")[-1]
                response = vimeo_client.get(f'https://api.vimeo.com/videos/{video_id}')
                response_json = response.json()
                st.markdown(response_json["link"])
                iframe = f'''
                <iframe src="{response_json["player_embed_url"]}" width="640" height="360" frameborder="0"
                allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
                '''
                st.markdown(iframe, unsafe_allow_html=True)
            
    # Agregar la respuesta del asistente al historial de mensajes
    st.session_state.messages.append({"role": "ASSISTANT", "content": answer})