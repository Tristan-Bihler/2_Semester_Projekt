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
            return []

        liked_genres = []
        for liked_title in favorite_movies_names:
            for movie in self.loaded_film_data:
                #print(movie["name"])
                #print(liked_title)
                if str(movie["name"]).strip().lower() == str(liked_title).strip():
                    liked_genres.extend(movie["genres"])
                    #print(liked_genres)
                    break
        
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        recommended_films = []
        for movie in self.loaded_film_data:
            movie_title = movie["name"]
            if movie_title in favorite_movies_names:
                continue

            score = 0
            for genre in movie["genres"]:
                score += genre_counts.get(genre, 0)

            if score > 0:
                recommendations_with_scores[movie_title] = score
        
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
            for user_ls in self.loaded_user_data:
                if str(user).lower().strip() == str(user_ls.get('name', '')).lower().strip():
                    found_user = True
                    if 'favorite_movies' in user_ls and isinstance(user_ls['favorite_movies'], list):
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
                    break
            
            if not found_user:
                print(f"User '{user}' not found in the database.")
                return False

            if movie_deleted:
                with open(self.user_db_path, 'w', encoding='utf-8') as f:
                    json.dump(self.loaded_user_data, f, ensure_ascii=False, indent=4)
                return True
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
                data = json.load(f)

            user_found = False
            if isinstance(data, list):
                for user in data:
                    if user.get("name").lower() == user_name_to_find:
                        #print(liked_movies)
                        liked_films = list(user.get("favorite_movies"))
                        #print(liked_films)
                        liked_films.append(liked_movies)
                        #print(liked_films)
                        user["favorite_movies"] = liked_films
                        user_found = True
                        print(f"User '{user_name_to_find}' updated successfully.")
                        break
                
                if not user_found:
                    print(f"User '{user_name_to_find}' not found in the file.")

                if user_found:
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
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"Warnung: Die Datei '{self.user_db_path}' enthält keine JSON-Liste. Initialisiere als leere Liste.")
                data = []

            data.append(new_user)

            with open(self.user_db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Benutzer '{user}' erfolgreich hinzugefügt.")
            
        except json.JSONDecodeError:
            print(f"Fehler: Die Datei '{self.user_db_path}' ist kein gültiges JSON. Setze sie auf eine leere Liste zurück.")
        except FileNotFoundError:
            print(f"Fehler: Die Datei '{self.user_db_path}' wurde nicht gefunden. Erstelle sie.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
