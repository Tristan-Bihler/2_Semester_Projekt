import json
from collections import Counter
import sys

#----------------------------------------------------Model
class Model():
    def __init__(self, user_db_path, films_db_path):
        self.user_db_path = user_db_path
        self.films_db_path = films_db_path

        self.loaded_user_data = self.load_json_data(self.user_db_path)
        self.loaded_film_data = self.load_json_data(self.films_db_path)

    def get_liked_films_from_jason(self, user):
        favorite_movies_names = []
        try:
            
            data = self.load_json_data(self.user_db_path)
            if isinstance(data, list):
                for favorite_movies in data:
                    print(user)
                    print(favorite_movies['name'])
                    if str(user).lower().strip() == str(favorite_movies['name']).lower().strip():
                        print("nice")
                        if isinstance(favorite_movies, dict) and 'favorite_movies' in favorite_movies:
                            for movie in favorite_movies['favorite_movies']:
                                favorite_movies_names.append(str(movie).lower())
                        else:
                            print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {favorite_movies}")
            else:
                print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(data)}")

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {self.user_db_path}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {self.user_db_path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        
        return favorite_movies_names
    
    def get_names_from_json(self):
        names = []
        try:
            if isinstance(self.loaded_user_data, list):
                for user in self.loaded_user_data:
                    if isinstance(user, dict) and 'name' in user:
                        names.append(str(user['name']).lower())
                    else:
                        print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
            else:
                print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(self.loaded_user_data)}")

        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return names

    def get_films_from_json(self):
        films = []
        try:
            if isinstance(self.loaded_film_data, list):
                for user in self.loaded_film_data:
                    if isinstance(user, dict) and 'name' in user:
                        films.append(str(user['name']))
                    else:
                        print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
            else:
                print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(self.loaded_film_data)}")
        except:
            print("Error")
        return films
    
    def load_json_data(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {path}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return data
    
    def get_recommendations(self, user):
        favorite_movies_names = []
        try:
            data = self.loaded_user_data
            for favorite_movies in data:
                print(user)
                print(favorite_movies)
                if str(user).lower().strip() == str(favorite_movies['name']).lower().strip():
                    print("nice")
                    for movie in favorite_movies['favorite_movies']:
                        favorite_movies_names.append(str(movie).lower())
                        print(favorite_movies_names)

        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        if not favorite_movies_names:
            return [] # Keine Empfehlungen, wenn keine Filme gemocht werden

        # Sammle alle Genres der gemochten Filme
        liked_genres = []
        for liked_title in favorite_movies_names:
            for movie in self.loaded_film_data:
                #print(movie["name"])
                #print(liked_title)
                if str(movie["name"]).strip().lower() == str(liked_title).strip():
                    liked_genres.extend(movie["genres"])
                    #print(liked_genres)
                    break
        
        # Zähle die Häufigkeit der Genres, um Präferenzen zu ermitteln
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        recommended_films = []
        for movie in self.loaded_film_data:
            movie_title = movie["name"]
            # Empfehle keine Filme, die bereits gemocht werden
            if movie_title in favorite_movies_names:
                continue

            score = 0
            # Berechne einen Score basierend auf übereinstimmenden Genres und deren Häufigkeit
            for genre in movie["genres"]:
                score += genre_counts.get(genre, 0) # Addiere die Häufigkeit des Genres

            if score > 0: # Nur Filme mit mindestens einer Genre-Übereinstimmung hinzufügen
                recommendations_with_scores[movie_title] = score
        
        # Sortiere Empfehlungen nach Score (absteigend)
        sorted_recommendations = sorted(recommendations_with_scores.items(), key=lambda item: item[1], reverse=True)
        #print(sorted_recommendations)
        for movie in sorted_recommendations:
            recommended_films.append(movie[0])
        #print(recommended_films)
        return recommended_films
    
    def removed_liked_films_from_jason(self, user, filename):
        found_user = False
        movie_deleted = False

        try:
            # Iterate through the list of user dictionaries
            for user_ls in self.loaded_user_data:
                # Check if the current user dictionary matches the target user
                if str(user).lower().strip() == str(user_ls.get('name', '')).lower().strip():
                    found_user = True
                    # Check if 'favorite_movies' key exists and is a list
                    if 'favorite_movies' in user_ls and isinstance(user_ls['favorite_movies'], list):
                        # Use a temporary list comprehension to create a new list
                        # without the item to be removed. This is safer than .remove()
                        # especially if 'filename' might not exist in the list.
                        initial_count = len(user_ls['favorite_movies'])
                        user_ls['favorite_movies'] = [
                            movie for movie in user_ls['favorite_movies']
                            if str(movie).lower().strip() != str(filename).lower().strip()
                        ]
                        if len(user_ls['favorite_movies']) < initial_count:
                            movie_deleted = True
                            print(f"Movie '{filename}' successfully deleted from {user}'s favorites.")
                        else:
                            print(f"Movie '{filename}' not found in {user}'s favorites.")
                    else:
                        print(f"User '{user}' has no 'favorite_movies' list or it's malformed.")
                    break # Exit the loop once the user is found and processed
            
            if not found_user:
                print(f"User '{user}' not found in the database.")
                return False # Indicate user not found

            # Only save if something was potentially changed (user found, and movie might have been deleted)
            if movie_deleted: # Only save if a movie was actually deleted
                with open(self.user_db_path, 'w', encoding='utf-8') as f:
                    json.dump(self.loaded_user_data, f, ensure_ascii=False, indent=4)
                # After direct save, also update the in-memory loaded_user_data for consistency
                return True # Indicate successful deletion
            else:
                return False


        except FileNotFoundError:
            print(f"Error: File not found at: {self.user_db_path}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file: {self.user_db_path}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
                
    def write_to_json(self, user_name_to_find, liked_movies):
        try:
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f) # json.load() for reading from file

            user_found = False
            # Ensure data is a list (expected format for multiple users)
            if isinstance(data, list):
                # 2. Find the user and 3. Modify their data
                for user in data:
                    if user.get("name").lower() == user_name_to_find:
                        #print(liked_movies)
                        liked_films = list(user.get("favorite_movies"))
                        #print(liked_films)
                        liked_films.append(liked_movies)
                        #print(liked_films)
                        user["favorite_movies"] = liked_films # Update existing keys or add new ones
                        user_found = True
                        print(f"User '{user_name_to_find}' updated successfully.")
                        break # Stop after finding and updating the first match
                
                if not user_found:
                    print(f"User '{user_name_to_find}' not found in the file.")

                # 4. Write the updated data back to the JSON file
                if user_found: # Only write back if a user was actually updated
                    with open(self.user_db_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    self.loaded_user_data = data
            else:
                print(f"Error: Expected JSON data to be a list, but found type: {type(data)}")

        
        except:
            print("Eror")
    
    def write_to_signup_json(self, user):
        new_user = {
            "id": "user_id",
            "name": user,
            "favorite_movies": []
        }
        try:
            # 1. Daten laden
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Sicherstellen, dass 'data' eine Liste ist
            if not isinstance(data, list):
                print(f"Warnung: Die Datei '{self.user_db_path}' enthält keine JSON-Liste. Initialisiere als leere Liste.")
                data = []

            # 2. Neuen Benutzer hinzufügen
            data.append(new_user)

            # 3. Daten speichern
            with open(self.user_db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Benutzer '{user}' erfolgreich hinzugefügt.")
            
        except json.JSONDecodeError:
            print(f"Fehler: Die Datei '{self.user_db_path}' ist kein gültiges JSON. Setze sie auf eine leere Liste zurück.")
        except FileNotFoundError:
            print(f"Fehler: Die Datei '{self.user_db_path}' wurde nicht gefunden. Erstelle sie.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
