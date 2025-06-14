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


    def get_json_data(self, key, user):
        data_list = []

        
        if key == "favorite_movies":
            if user != None:
                for data_block in self.load_json_data(self.user_db_path):
                    if str(user).lower().strip() == str(data_block["name"]).lower().strip():
                        if isinstance(data_block, dict) and key in data_block:
                            for data_word in data_block[key]:
                                data_list.append(str(data_word))
                        else:
                            print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {data_block}")

        elif key == "name":
            if user == None:
                for user in self.load_json_data(self.user_db_path):
                    if isinstance(user, dict) and key in user:
                        data_list.append(str(user[key]).lower())
                    else:
                        print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")


        elif key == "film_names":
            for user in self.loaded_film_data:
                if isinstance(user, dict) and key in user:
                    data_list.append(str(user[key]))
                else:
                    print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
        
        return data_list

    def load_json_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data
    
    def removed_liked_films_from_jason(self, user, filename):
        found_user = False
        movie_deleted = False

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
                
    def write_to_json(self, user_name_to_find, liked_movies):
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
    
    def write_to_signup_json(self, user):
        new_user = {
            "id": "user_id",
            "name": user,
            "favorite_movies": []
        }
        with open(self.user_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"Warnung: Die Datei '{self.user_db_path}' enthält keine JSON-Liste. Initialisiere als leere Liste.")
            data = []

        data.append(new_user)

        with open(self.user_db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Benutzer '{user}' erfolgreich hinzugefügt.")
    
    def get_recommendations(self, user):
        favorite_movies_names = []
        
        #Lieblingsfilme der Nutzer in eine Variable gepseichert
        favorite_movies_names = self.get_json_data("favorite_movies", user)

        #Überprüft ob es auch Daten hat, sonst unterbricht es hier die  Funktion
        if not favorite_movies_names:
            return []

        #Alle Genre in den gespeicherten Filme rausfiltern
        liked_genres = []
        for liked_title in favorite_movies_names:
            for movie in self.loaded_film_data:
                #print(movie["name"])
                #print(liked_title)
                if str(movie["film_names"]).strip() == str(liked_title).strip():
                    liked_genres.extend(movie["genres"])
                    #print(liked_genres)
                    break
        
        #Die Genre zählen und in eine Dictionary aufbewahren
        genre_counts = Counter(liked_genres)

        #Initliaiserung jeglicher Variablen
        recommendations_with_scores = {}
        recommended_films = []
        
        #Für jeden Film mit dem selben Genre rausfiltern, solange es nicht innerhalb der schon ausgewählten Filme ist
        for movie in self.loaded_film_data:
            movie_title = movie["film_names"]
            if movie_title in favorite_movies_names:
                continue #Ist der Film in der Liste, dann überspringe den rest und führe die For Schleife weiter

            score = 0
            #Genre für jeden Film zhäeln und der score Liste hinzufügen 
            for genre in movie["genres"]:   
                score += genre_counts.get(genre, 0)

            if score > 0:
                recommendations_with_scores[movie_title] = score
        
        #Genre nach aufzählung sortieren und jeglichen Film zu dem Genre finden und der Dictionary hinzufügen
        #Ergebnis ist eine nach genre gezählte und von höchstem bis zum niedrigsten Genre Wert der Dictionary hinzugefügt
        sorted_recommendations = sorted(recommendations_with_scores.items(), key=lambda item: item[1], reverse=True)
        #print(sorted_recommendations)

        #Jeden Film der Dictionary, den Titel der recommended Liste hinzugefügt
        for movie in sorted_recommendations:
            recommended_films.append(movie[0])
        #print(recommended_films)
        return recommended_films
    

    #--------------------------------------------------------------------

    def create_film_genre_mapping(self, films_data):
        """Creates a dictionary mapping film_id to its genres."""
        film_genres = {}
        for film in films_data:
            film_genres[film['film_names']] = set(film['genres']) # Using set for faster operations later
        return film_genres

    def calculate_user_genre_profiles(self, users_data, film_genres_map):
        """Calculates the genre profile (set of genres) for each user."""
        user_genre_profiles = {}
        for user in users_data:
            user_id = str(user['name']).lower()
            watched_films = user['favorite_movies']
            user_genres = set()
            for film_id in watched_films:
                if film_id in film_genres_map:
                    user_genres.update(film_genres_map[film_id])
            user_genre_profiles[user_id] = user_genres
        return user_genre_profiles

    def jaccard_similarity(self, set1, set2):
        """Calculates the Jaccard similarity between two sets."""
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        if union == 0:
            return 0.0 # Avoid division by zero
        return intersection / union

    def get_user_base_recommendations(self, target_user_id):
        """
        Recommends films to a target user based on genre similarity to other users.
        """
        users_data = self.load_json_data(self.user_db_path)
        films_data = self.load_json_data(self.films_db_path)
        film_genres_map = self.create_film_genre_mapping(films_data)
        user_genre_profiles = self.calculate_user_genre_profiles(users_data, film_genres_map)

        if target_user_id not in user_genre_profiles:
            print(f"Error: Target user '{target_user_id}' not found.")
            return []

        target_user_genres = user_genre_profiles[target_user_id]
        target_user_watched_films = next(user['favorite_movies'] for user in users_data if str(user['name']).lower() == target_user_id)

        similarities = []
        for user_id, genres in user_genre_profiles.items():
            if user_id == target_user_id:
                continue
            
            sim = self.jaccard_similarity(target_user_genres, genres)
            similarities.append((sim, user_id))

        # Sort by similarity in descending order
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Get the closest matching user (you can adjust this to get top N users)
        if not similarities:
            print("No other users to compare with.")
            return []

        closest_match_user_id = similarities[0][1]
        
        # Get films from the closest matching user
        closest_match_user_films = next(user['favorite_movies'] for user in users_data if (user['name']).lower() == closest_match_user_id)

        # Filter out films the target user has already watched
        recommended_films = [
            film_id for film_id in closest_match_user_films 
            if film_id not in target_user_watched_films
        ]

        return recommended_films