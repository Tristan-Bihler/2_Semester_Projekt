#----------------------------------------------------Model
import json
from collections import Counter
import sys

class Model:
    """
    Das Model verwaltet die Daten und die Geschäftslogik der Anwendung.
    Es hat keine Kenntnis von der View oder dem Controller.
    """
    def __init__(self, users_filepath, films_filepath):
        self.users_filepath = users_filepath
        self.films_filepath = films_filepath
        self._all_films_data = self._load_json_data(self.films_filepath) # Lade Filmdaten einmalig
        self._all_users_data = self._load_json_data(self.users_filepath) # Lade Benutzerdaten einmalig

    def _load_json_data(self, filepath):
        """
        Lädt JSON-Daten aus einer Datei.
        Gibt eine Fehlermeldung aus und beendet das Programm bei schwerwiegenden Fehlern.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                # Wenn das Top-Level-Element keine Liste ist, werfen wir einen Fehler
                raise ValueError(f"Die JSON-Datei {filepath} enthält keine Liste auf der obersten Ebene. Typ: {type(data)}")
            return data
        except FileNotFoundError:
            # Fataler Fehler: Datei nicht gefunden, Anwendung kann nicht funktionieren
            print(f"Fehler: Datei nicht gefunden unter: {filepath}. Programm wird beendet.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            # Fataler Fehler: Ungültiges JSON-Format, Anwendung kann nicht funktionieren
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}. Programm wird beendet.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            # Alle anderen unerwarteten Fehler
            print(f"Ein unerwarteter Fehler ist beim Laden von {filepath} aufgetreten: {e}. Programm wird beendet.", file=sys.stderr)
            sys.exit(1)

    def get_all_films_data(self):
        """Gibt alle geladenen Filmdaten zurück."""
        return self._all_films_data

    def get_all_users_data(self):
        """Gibt alle geladenen Benutzerdaten zurück."""
        return self._all_users_data

    def get_user_favorite_movies(self, username):
        """
        Sucht die Lieblingsfilme eines bestimmten Benutzers.
        Gibt eine Liste der Titel der Lieblingsfilme zurück.
        """
        favorite_movies_names = []
        for user_data in self._all_users_data:
            if isinstance(user_data, dict) and 'name' in user_data:
                if str(username).lower().strip() == str(user_data['name']).lower().strip():
                    if 'favorite_movies' in user_data and isinstance(user_data['favorite_movies'], list):
                        for movie in user_data['favorite_movies']:
                            favorite_movies_names.append(str(movie).lower())
                    return favorite_movies_names # Benutzer gefunden, gib seine Filme zurück
        return [] # Benutzer nicht gefunden oder keine Lieblingsfilme

    def get_recommendations(self, liked_movie_titles):
        """
        Berechnet Filmempfehlungen basierend auf den vom Benutzer gemochten Filmen.
        Verwendet die Genres der Lieblingsfilme, um ähnliche Filme zu finden.
        """
        if not liked_movie_titles:
            return [] # Keine Empfehlungen, wenn keine Filme gemocht werden

        liked_genres = []
        for liked_title in liked_movie_titles:
            for movie in self._all_films_data:
                if str(movie.get("name", "")).strip().lower() == str(liked_title).strip():
                    if "genre" in movie and isinstance(movie["genre"], list):
                        liked_genres.extend(movie["genre"])
                    break
        
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        for movie in self._all_films_data:
            movie_title = movie.get("name", "")
            if not movie_title: # Film ohne Titel ignorieren
                continue

            # Empfehle keine Filme, die bereits gemocht werden
            if movie_title.lower() in [title.lower() for title in liked_movie_titles]:
                continue

            score = 0
            # Berechne einen Score basierend auf übereinstimmenden Genres und deren Häufigkeit
            for genre in movie.get("genre", []):
                score += genre_counts.get(genre, 0)

            if score > 0: # Nur Filme mit mindestens einer Genre-Übereinstimmung hinzufügen
                recommendations_with_scores[movie_title] = score
        
        # Sortiere Empfehlungen nach Score (absteigend)
        sorted_recommendations = sorted(recommendations_with_scores.items(), key=lambda item: item[1], reverse=True)
        return [title for title, score in sorted_recommendations]

    def validate_user(self, username):
        """Prüft, ob ein Benutzer im System existiert."""
        for user_data in self._all_users_data:
            if isinstance(user_data, dict) and 'name' in user_data:
                if str(username).lower().strip() == str(user_data['name']).lower().strip():
                    return True
        return False

    def add_new_user(self, username):
        """
        Fügt einen neuen Benutzer zur Benutzerdatenbank hinzu.
        Gibt True bei Erfolg, False wenn der Benutzer bereits existiert.
        """
        if self.validate_user(username):
            return False # Benutzer existiert bereits

        new_user_data = {"name": username, "favorite_movies": []}
        self._all_users_data.append(new_user_data)
        
        try:
            with open(self.users_filepath, 'w', encoding='utf-8') as f:
                json.dump(self._all_users_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern des neuen Benutzers: {e}", file=sys.stderr)
            return False