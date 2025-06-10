# Dieses immersive Dokument demonstriert ein einfaches Beispiel für
# Inhaltsbasierte Filterung in Python.

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create_item_features(items_df):

    items_df['description'] = items_df['description'].fillna('')

    tfidf = TfidfVectorizer(stop_words='english') # Ignoriert englische Stoppwörter
    tfidf_matrix = tfidf.fit_transform(items_df['description'])
    return tfidf_matrix, tfidf

def get_content_similarity(tfidf_matrix):

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def recommend_items_content_based(item_id, items_df, cosine_sim, num_recommendations=2):

    idx = items_df[items_df['id'] == item_id].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    item_indices = [i[0] for i in sim_scores]

    return items_df['title'].iloc[item_indices].tolist()

if __name__ == "__main__":
    data = {
        'id': [1, 2, 3, 4, 5],
        'title': ['Film A: Action & Sci-Fi', 'Film B: Romantic Comedy', 'Film C: Sci-Fi Adventure',
                  'Film D: Drama & Thriller', 'Film E: Romantic Drama'],
        'description': [
            'Ein spannender Film voller Action und Science-Fiction. Roboter kämpfen gegen Menschen.',
            'Eine herzerwärmende romantische Komödie über Liebe und Freundschaft.',
            'Ein episches Science-Fiction-Abenteuer im Weltraum mit Aliens und Raumschiffen.',
            'Ein düsteres Drama mit psychologischem Thriller-Element und unerwarteten Wendungen.',
            'Ein gefühlvolles romantisches Drama über verbotene Liebe und Schicksal.'
        ]
    }
    items_df = pd.DataFrame(data)

    print("--- Elementdaten ---")
    print(items_df)
    print("\n")

    tfidf_matrix, tfidf_vectorizer = create_item_features(items_df)
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
    print("\n")

    cosine_sim = get_content_similarity(tfidf_matrix)
    print("Kosinus-Ähnlichkeitsmatrix (erste 3x3):")
    print(cosine_sim[:3, :3])
    print("\n")

    item_to_recommend_for = 1
    recommendations_film_a = recommend_items_content_based(item_to_recommend_for, items_df, cosine_sim)
    print(f"Empfehlungen für '{items_df[items_df['id'] == item_to_recommend_for]['title'].iloc[0]}': {recommendations_film_a}")

    item_to_recommend_for_2 = 2
    recommendations_film_b = recommend_items_content_based(item_to_recommend_for_2, items_df, cosine_sim)
    print(f"Empfehlungen für '{items_df[items_df['id'] == item_to_recommend_for_2]['title'].iloc[0]}': {recommendations_film_b}")
