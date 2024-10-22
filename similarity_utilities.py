import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from clients import openai_client

def generate_embeddings(text):
    response = openai_client.embeddings.create(
    input=text,
    model="text-embedding-3-small")

    return response.data[0].embedding

def search_similar_questions(query_text, context_db, k=10):
    vector_db = pd.read_parquet(f'{context_db}.parquet')

    query_embedding = generate_embeddings(query_text)

    embeddings = np.stack(vector_db['Embedding'].values)

    similarities = cosine_similarity([query_embedding], embeddings)[0]

    top_k_indices = np.argsort(similarities)[-k:][::-1]

    top_sources = vector_db.iloc[top_k_indices]['Source'].unique()
    top_answers = vector_db.iloc[top_k_indices]['Answer'].tolist()
    top_questions = vector_db.iloc[top_k_indices]['Question'].tolist()

    return top_sources, top_questions, top_answers
