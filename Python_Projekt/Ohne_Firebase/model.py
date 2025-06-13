import json
from collections import Counter
import sys

#----------------------------------------------------Model
class Model():
    def __init__(self, user_db_path, films_db_path):
        self.user_db_path = user_db_path
        self.films_db_path = films_db_path
        
    def load(file):
        try:
            with open(file) as in_file:
                loaded_txt = in_file.read().lower().strip("").split('\n')
                    
                return loaded_txt
            
        except IOError as e:
            print("{}\nError opening {}. Terminating program.".format(e, file),
                file=sys.stderr)
            sys.exit(1)

    def get_recommended_films_from_json(self, user):
        favorite_movies_names = []
        try:
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
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
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                for user in data:
                    if isinstance(user, dict) and 'name' in user:
                        names.append(str(user['name']).lower())
                    else:
                        print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
            else:
                print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(data)}")

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {self.user_db_path}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {self.user_db_path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return names


    def get_films_from_json(self):
        films = []
        try:
            with open(self.films_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                for user in data:
                    if isinstance(user, dict) and 'name' in user:
                        films.append(str(user['name']))
                    else:
                        print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
            else:
                print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(data)}")

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {self.films_db_path}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {self.films_db_path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return films
    
    def get_json(self):
        films = []
        try:
            with open(self.films_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {self.films_db_path}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {self.films_db_path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return data
    
    def get_recommendations(self, user):
        favorite_movies_names = []
        try:
            with open(self.user_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
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

        if not favorite_movies_names:
            return [] # Keine Empfehlungen, wenn keine Filme gemocht werden

        # Sammle alle Genres der gemochten Filme
        liked_genres = []
        for liked_title in favorite_movies_names:
            for movie in self.get_json():
                #print(movie["name"])
                #print(liked_title)
                if str(movie["name"]).strip().lower() == str(liked_title).strip():
                    liked_genres.extend(movie["genre"])
                    break
        
        # Zähle die Häufigkeit der Genres, um Präferenzen zu ermitteln
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        recommended_films = []
        for movie in self.get_json():
            movie_title = movie["name"]
            # Empfehle keine Filme, die bereits gemocht werden
            if movie_title in favorite_movies_names:
                continue

            score = 0
            # Berechne einen Score basierend auf übereinstimmenden Genres und deren Häufigkeit
            for genre in movie["genre"]:
                score += genre_counts.get(genre, 0) # Addiere die Häufigkeit des Genres

            if score > 0: # Nur Filme mit mindestens einer Genre-Übereinstimmung hinzufügen
                recommendations_with_scores[movie_title] = score
        
        # Sortiere Empfehlungen nach Score (absteigend)
        sorted_recommendations = sorted(recommendations_with_scores.items(), key=lambda item: item[1], reverse=True)
        for movie in sorted_recommendations:
            recommended_films.append(movie[0])
        #print(recommended_films)
        return recommended_films
    
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
                        print(liked_movies)
                        liked_films = list(user.get("favorite_movies"))
                        print(liked_films)
                        liked_films.append(liked_movies)
                        print(liked_films)
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
            else:
                print(f"Error: Expected JSON data to be a list, but found type: {type(data)}")

        
        except:
            print("Eror")
