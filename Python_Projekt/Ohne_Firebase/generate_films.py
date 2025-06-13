import requests
import json

def get_tmdb_data(api_key, num_pages=1):
    """
    Holt Filmdaten (Name, Beschreibung, Genres) von TMDB.

    Args:
        api_key (str): Dein TMDB API-Schlüssel.
        num_pages (int): Die Anzahl der Seiten mit Filmen, die abgerufen werden sollen.
                         Jede Seite enthält standardmäßig 20 Filme.

    Returns:
        list: Eine Liste von Dictionaries, wobei jedes Dictionary einen Film darstellt.
              Gibt eine leere Liste zurück, wenn ein Fehler auftritt.
    """
    base_url = "https://api.themoviedb.org/3"
    movies_data = []

    # Zuerst alle Genres abrufen, da die Filmdaten nur Genre-IDs enthalten
    genres_url = f"{base_url}/genre/movie/list?api_key={api_key}&language=de-DE"
    try:
        genres_response = requests.get(genres_url)
        genres_response.raise_for_status()  # Wirft einen Fehler für schlechte Statuscodes
        genres_data = genres_response.json()
        genre_map = {genre['id']: genre['name'] for genre in genres_data['genres']}
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Genres: {e}")
        return []

    for page in range(1, num_pages + 1):
        # Beispiel: Beliebte Filme abrufen. Du kannst auch andere Endpunkte verwenden.
        # Siehe TMDB API-Dokumentation für weitere Optionen: https://developers.themoviedb.org/3/
        url = f"{base_url}/movie/popular?api_key={api_key}&language=de-DE&page={page}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Wirft einen Fehler für schlechte Statuscodes (4xx oder 5xx)
            data = response.json()

            for movie in data['results']:
                movie_info = {
                    "name": movie.get('title'),
                    "beschreibung": movie.get('overview'),
                    "genres": [genre_map.get(genre_id) for genre_id in movie.get('genre_ids', []) if genre_map.get(genre_id) is not None],
                    "youtubeTrailerUrl": f"https://www.youtube.com/results?search_query={movie.get('title').replace(' ', '%20')}"
                }
                movies_data.append(movie_info)

        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Abrufen von Filmen auf Seite {page}: {e}")
            break  # Schleife beenden, wenn ein Fehler auftritt
        except json.JSONDecodeError as e:
            print(f"Fehler beim Dekodieren der JSON-Antwort auf Seite {page}: {e}")
            break

    return movies_data

def save_to_json(data, filename="tmdb_movies2.json"):
    """
    Speichert eine Liste von Dictionaries in einer JSON-Datei.

    Args:
        data (list): Die zu speichernden Daten.
        filename (str): Der Name der Ausgabedatei.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Daten erfolgreich in '{filename}' gespeichert.")
    except IOError as e:
        print(f"Fehler beim Speichern der Datei: {e}")

if __name__ == "__main__":
    # ERSETZE DIES DURCH DEINEN EIGENEN TMDB API-SCHLÜSSEL!
    your_tmdb_api_key = "1009189381ece1b4beabf311068e73af"

    if your_tmdb_api_key == "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMDA5MTg5MzgxZWNlMWI0YmVhYmYzMTEwNjhlNzNhZiIsIm5iZiI6MTc0OTgwMjE2Ny4yNiwic3ViIjoiNjg0YmRjYjdmN2Q3Njc2NTA4NWM3MzIzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9._QsNJ-SUmLVsvPO9YE8cshUgZCns4o1mlxZfH48bFuQ":
        print("Bitte ersetze 'DEIN_TMDB_API_SCHLÜSSEL_HIER' durch deinen tatsächlichen TMDB API-Schlüssel.")
    else:
        # Wie viele Seiten von Filmen möchtest du abrufen?
        # Jede Seite enthält 20 Filme. 5 Seiten = 100 Filme.
        num_pages_to_fetch = 5
        print(f"Abrufen von {num_pages_to_fetch} Seiten mit Filmen von TMDB...")
        movies = get_tmdb_data(your_tmdb_api_key, num_pages=num_pages_to_fetch)

        if movies:
            save_to_json(movies)
        else:
            print("Keine Filme zum Speichern gefunden oder es gab Fehler beim Abrufen der Daten.")
