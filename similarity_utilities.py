import google.generativeai as genai
import os
import faiss
import numpy as np
import pickle

# Cargar el índice Faiss
index = faiss.read_index('faiss.index')

# Cargar los nombres de los documentos
with open('document_names.pkl', 'rb') as f:
    document_names = pickle.load(f)

def generate_embedding(text):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
        title="Embedding of single string")
    return result["embedding"]

def search_similar_documents(query_text, k=5):
    # Generar el embedding de la query
    query_embedding = generate_embedding(query_text)
    
    # Convertir el embedding de la query a numpy y buscar los k más similares
    query_embedding = np.array([query_embedding])
    distances, indices = index.search(query_embedding, k)
    
    # Recuperar los nombres de los documentos más similares usando los índices
    similar_documents = [document_names[i] for i in indices[0]]
    return similar_documents, distances[0]