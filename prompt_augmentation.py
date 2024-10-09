from similarity_utilities import search_similar_documents
import os

def generate_augmented_prompt(prompt):
    # Buscar los 5 documentos más relevantes
    top_documents, top_distances = search_similar_documents(prompt)
    
    # Inicializar el augmented prompt con la información básica y el prompt del usuario
    augmented_prompt = f"""
    Responde como Klopp, un amable y servicial asistente AI especializado en finanzas personales. Se te proveerán 5 transcripciones 
    de videos, y debes escoger el contenido más relevante para aconsejar o responder al usuario.

    Pregunta del usuario: '{prompt}'

    Transcripciones de Referencias:
    """
    
    # Leer y añadir el contenido de cada documento relevante al prompt
    for doc_path in top_documents:
        with open(os.path.join("textos", doc_path), 'r', encoding='utf-8') as f:
            doc_content = f.read()
            # Añadir cada transcripción al prompt, con una separación clara
            augmented_prompt += f"\n---\nTranscripción de {doc_path}:\n{doc_content}\n"

    # Devolver el augmented prompt completo con los contenidos añadidos
    return augmented_prompt
