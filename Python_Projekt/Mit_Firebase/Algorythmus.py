# Dieses immersive Dokument demonstriert ein einfaches Beispiel für
# Inhaltsbasierte Filterung in Python.

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create_item_features(items_df):
    """
    Erstellt Feature-Vektoren für Elemente basierend auf ihren Textbeschreibungen.
    Hier wird TF-IDF verwendet.

    Parameter:
    items_df (pd.DataFrame): DataFrame mit Elementen und ihren Merkmalen (z.B. 'description' Spalte).

    Rückgabe:
    tuple: (tfidf_matrix, tfidf_vectorizer)
           tfidf_matrix (scipy.sparse.csr_matrix): TF-IDF-Matrix der Elementmerkmale.
           tfidf_vectorizer (TfidfVectorizer): Der trainierte TF-IDF-Vektorisierer.
    """
    # Wenn die Beschreibung nicht existiert oder leer ist, ersetzen Sie sie durch einen leeren String
    items_df['description'] = items_df['description'].fillna('')

    tfidf = TfidfVectorizer(stop_words='english') # Ignoriert englische Stoppwörter
    tfidf_matrix = tfidf.fit_transform(items_df['description'])
    return tfidf_matrix, tfidf

def get_content_similarity(tfidf_matrix):
    """
    Berechnet die Kosinus-Ähnlichkeit zwischen den Elementen basierend auf ihrer TF-IDF-Matrix.

    Parameter:
    tfidf_matrix (scipy.sparse.csr_matrix): TF-IDF-Matrix der Elementmerkmale.

    Rückgabe:
    numpy.ndarray: Eine Matrix der Elementähnlichkeit.
    """
    # linearen Kernel ist äquivalent zur Kosinus-Ähnlichkeit, wenn Features normalisiert sind
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def recommend_items_content_based(item_id, items_df, cosine_sim, num_recommendations=2):
    """
    Generiert Empfehlungen für ein bestimmtes Element basierend auf
    inhaltsbasierter Filterung.

    Parameter:
    item_id (int): Die ID des Elements, für das Empfehlungen generiert werden sollen.
    items_df (pd.DataFrame): DataFrame mit Elementinformationen (muss 'id' und 'title' haben).
    cosine_sim (numpy.ndarray): Matrix der Elementähnlichkeit.
    num_recommendations (int): Anzahl der zu empfehlenden Elemente.

    Rückgabe:
    list: Eine Liste der empfohlenen Elementtitel.
    """
    # Holt den Index des Elements anhand seiner ID
    idx = items_df[items_df['id'] == item_id].index[0]

    # Holt die Ähnlichkeitswerte des Elements mit allen anderen Elementen
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sortiert die Elemente basierend auf den Ähnlichkeitswerten
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Holt die Ähnlichkeitswerte der 10 ähnlichsten Elemente (ohne sich selbst)
    # Wir nehmen hier 10, um sicherzustellen, dass wir genug Elemente haben,
    # auch wenn einige schon vom Benutzer gesehen wurden oder das gleiche Element sind.
    sim_scores = sim_scores[1:11] # Überspringt das erste Element, da es das Element selbst ist

    # Holt die Indizes der Elemente
    item_indices = [i[0] for i in sim_scores]

    # Gibt die Titel der empfohlenen Elemente zurück
    return items_df['title'].iloc[item_indices].tolist()

if __name__ == "__main__":
    # Beispiel-Elementdaten (z.B. Filme mit Beschreibungen)
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

    # Erstellt Feature-Vektoren
    tfidf_matrix, tfidf_vectorizer = create_item_features(items_df)
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
    # print(tfidf_matrix.toarray()) # Kann bei großen Matrizen viel Platz beanspruchen
    print("\n")

    # Berechnet die Inhaltsähnlichkeit zwischen den Elementen
    cosine_sim = get_content_similarity(tfidf_matrix)
    print("Kosinus-Ähnlichkeitsmatrix (erste 3x3):")
    print(cosine_sim[:3, :3]) # Zeigt nur einen kleinen Ausschnitt
    print("\n")

    # Empfehlungen für 'Film A' (ID 1)
    item_to_recommend_for = 1
    recommendations_film_a = recommend_items_content_based(item_to_recommend_for, items_df, cosine_sim)
    print(f"Empfehlungen für '{items_df[items_df['id'] == item_to_recommend_for]['title'].iloc[0]}': {recommendations_film_a}")

    # Empfehlungen für 'Film B' (ID 2)
    item_to_recommend_for_2 = 2
    recommendations_film_b = recommend_items_content_based(item_to_recommend_for_2, items_df, cosine_sim)
    print(f"Empfehlungen für '{items_df[items_df['id'] == item_to_recommend_for_2]['title'].iloc[0]}': {recommendations_film_b}")
