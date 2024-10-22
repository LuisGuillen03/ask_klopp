from similarity_utilities import search_similar_questions
import os

def generate_augmented_prompt(prompt, context_db):
    # Buscar los 10 documentos más relevantes
    top_sources, top_questions, top_answers = search_similar_questions(prompt, context_db)

    # Inicializar el prompt enriquecido con contexto relevante
    augmented_prompt = f"""Responde como Klopp, un amable y servicial asistente AI especializado en finanzas personales. 
    Se te proveerán 10 preguntas y respuestas previas, que pueden ser relevantes para aconsejar o responder al usuario (No les hagas referencia en tu respuesta).

    Pregunta del usuario: '{prompt}'

    Preguntas y Respuestas Relevantes:
    """
    
    # Añadir las preguntas y respuestas relevantes al prompt
    for i, (question, answer) in enumerate(zip(top_questions, top_answers), 1):
        augmented_prompt += f"\nReferencia {i}:\n- **Pregunta**: {question}\n- **Respuesta**: {answer}\n"

    return top_sources, augmented_prompt
