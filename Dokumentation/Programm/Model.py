import json
from collections import Counter
import sys

#----------------------------------------------------Model
class Model():
    def __init__(self, user_db_path, films_db_path):
        #Pfade für die Datenbanken festlegen
        self.user_db_path = user_db_path
        self.films_db_path = films_db_path

        #Daten Laden sodass diese nicht während dem programm immerwieder geladen werden müssen
        self.loaded_user_data = self.load_json_data(self.user_db_path)
        self.loaded_film_data = self.load_json_data(self.films_db_path)

    #-----------------------------------------------Datenbank Verwaltungs Funktionen
    def get_json_data(self, key, user):
        #Funktion für das laden der Daten mit einem key aus den Datenbanken
        data_list = []

        #Abfrage ob der key den der Favoriten Filme entspricht
        if key == "favorite_movies":
            #Abfrage ob auch ein user vorhanden ist
            if user != None:
                #Jeden Datenblock durchgehen
                for data_block in self.load_json_data(self.user_db_path):
                    #Abfrage des user namens mit dem name aus dem Datenblock und dem key name
                    if str(user).lower().strip() == str(data_block["name"]).lower().strip():
                        if isinstance(data_block, dict) and key in data_block:
                            for data_word in data_block[key]:
                                data_list.append(str(data_word))
                        else:
                            raise Exception("Ungültiges Benutzerobjekt gefunden: {user}")
                            #print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {data_block}")
            else:
                raise Exception("Nutzer fehlt")

        #Abfrage ob der key den der name entspricht, somit die Nutzernamen dann auch zurückgegeben werden können
        elif key == "name":
            if user == None:
                for user in self.load_json_data(self.user_db_path):
                    if isinstance(user, dict) and key in user:
                        data_list.append(str(user[key]).lower())
                    else:
                        raise Exception("Ungültiges Benutzerobjekt gefunden: {user}")
                        #print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")

        #Abfrage ob der key den der Film Namen entspricht, somit die Filmnamen dann auch zurückgegeben werden können
        elif key == "film_names":
            for user in self.loaded_film_data:
                if isinstance(user, dict) and key in user:
                    data_list.append(str(user[key]))
                else:
                    raise Exception("Ungültiges Benutzerobjekt gefunden: {user}")
                    #print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
        
        return data_list

    #Alle möglichen Daten aus einer Json Datei laden
    def load_json_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data
    
    #Funktion für das löschen bestimmter Filme aus der Favoriten Liste des eingeloggten Nutzers
    def removed_liked_films_from_jason(self, user, filename):
        found_user = False
        movie_deleted = False

        #Jeden Nutzer der Nutzerliste durchgehen
        for user_ls in self.loaded_user_data:
            #Den eingeloggten Nutzer in der Nutzerliste Finden
            if str(user).lower().strip() == str(user_ls['name']).lower().strip():
                found_user = True
                #Die Favoriten Liste des Nutzers abgreifen
                if 'favorite_movies' in user_ls and isinstance(user_ls['favorite_movies'], list):
                    #Die Länge der Liste bestimmen
                    initial_count = len(user_ls['favorite_movies'])
                    #Die geladene List den zu entfernenden Film finden und anschließend löschen.
                    user_ls['favorite_movies'] = [
                        movie for movie in user_ls['favorite_movies']
                        if str(movie).lower().strip() != str(filename).lower().strip()
                    ]
                    if len(user_ls['favorite_movies']) < initial_count:
                        movie_deleted = True
                        #print(f"Movie '{filename}' successfully deleted from {user}'s favorites.")
                    else:
                        raise Exception(f"{filename} nicht gefunden")
                        #print(f"Movie '{filename}' not found in {user}'s favorites.")
                else:
                    raise Exception("Daten Falsch gegeben")
                break
        
        if not found_user:
            raise Exception(f"{user} nicht gefunden")

        if movie_deleted:
            with open(self.user_db_path, 'w', encoding='utf-8') as f:
                json.dump(self.loaded_user_data, f, indent=4)#die argumente nach data macht die Json lesbarer
            return True
        else:
            raise Exception(f"{filename} konnte nicht gelöscht werden")
                
    def write_to_json(self, user_name_to_find, liked_movies):
        with open(self.user_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_found = False
        if isinstance(data, list):#Überprüfen dass data auch eine liste ist
            #jeden Nutzer durchgehen und den eingeloggten nutzer finden
            for user in data:
                if user.get("name").lower() == user_name_to_find:
                    #Die gemochteten Filne den Favoriten Liste hinzufügen
                    #print(liked_movies)
                    liked_films = list(user.get("favorite_movies"))
                    #print(liked_films)
                    liked_films.append(liked_movies)
                    #print(liked_films)
                    user["favorite_movies"] = liked_films
                    user_found = True
                    #print(f"User '{user_name_to_find}' updated successfully.")
                    break
            
            #Wenn der nutzer in der Liste nicht gefunden wurdem den Fehler melden
            if not user_found:
                raise Exception("Nutzer nicht geunden")

            #Wenn der nutzer gefunden wurde, die Daten in die Nutzer Json laden
            if user_found:
                with open(self.user_db_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)#die argumente nach data macht die Json lesbarer
                self.loaded_user_data = data
        else:
            raise Exception("Daten sind fehlerhaft")
        
    def write_to_signup_json(self, user):
        #Bei dem erstellen eines neuen nutzer eine Vorlage erstellen und die, mit den Nutzer Namen, in die User.json Datenbank reinschreiben
        #Nutzer Block
        new_user = {
            "name": user,
            "favorite_movies": []
        }
        with open(self.user_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        #Überprügen ob die Datenbank auch gefunden wurde und den richtigen Tyo hat, in diesem Fall eine Liste
        if not isinstance(data, list):
            data = []
            raise Exception("Datenbank nicht gefunden")

        #Den neuen Nutzer Block der Datenbank hinzufügen
        data.append(new_user)

        #Die neue Daten in die Json schreiben, da wir alle daten rausschreiben und den nutzer hinzufügen, tun wir alle Daten auch wieder überscheiben
        with open(self.user_db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)#die argumente nach data macht die Json lesbarer
        #print(f"Benutzer '{user}' erfolgreich hinzugefügt.")


    #-----------------------------------------------Content based Algorithmus
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
    


    #--------------------------------------------------------------------Colaborativ Algorithmus
    def create_film_genre_mapping(self, films_data):
        """
        Für jeden Film von films_data soll es zu jedem Film ein satz genres aus der film liste, für den film, film_genres hinzufügen
        """
        film_genres = {}
        for film in films_data:
            film_genres[film['film_names']] = set(film['genres']) #Film genres ist eine Dictionary, erkennt man an den {} klammern bei der initialisierung
        return film_genres

    def calculate_user_genre_profiles(self, users_data, film_genres_map):
        """für jeden user in user_data, also der user Liste, soll es den namen des users und dessen lieblingsfilme entnehmen"""
        user_genre_profiles = {}
        #Jeden Nutzer durchgehen
        for user in users_data:
            user_id = str(user['name']).lower()
            liked_films = user['favorite_movies']
            user_genres = set()
            #Jeden Film in der Favoriten Liste des Users durchgehen
            for film_id in liked_films:
                #Falls der Film in der Genre Liste vorkommt, ---------
                if film_id in film_genres_map:
                    user_genres.update(film_genres_map[film_id])
            user_genre_profiles[user_id] = user_genres
        return user_genre_profiles

    def jaccard_similarity(self, set1, set2):
        """Überprüft wie ähnlich die beiden genres listen der user sind und gibt die ähnlichkeit durch return zurück"""
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        if union == 0:
            return 0.0 # Somit es nicht ausversehen Durch 0 devidiert
        return intersection / union

    def get_user_base_recommendations(self, target_user_id):
        """
        Als erstes holt es sich die benötigten daten und wandelt diese für das Colaborativ_based_Algorythm um.
        Als nächstes überprüft es, ob es den user überhaupt gibt -> Hilfreich für debugging
        """
        #Daten Herholen
        users_data = self.load_json_data(self.user_db_path)
        films_data = self.load_json_data(self.films_db_path)
        
        #Daten Umwandeln
        #Genre rausfiltern
        film_genres_map = self.create_film_genre_mapping(films_data)

        #Es generiert für alle Nutzer eine Genre Lsite und fügt diese user_genres_profiles zu
        user_genre_profiles = self.calculate_user_genre_profiles(users_data, film_genres_map)

        #Sinvoll für das Debugging -> Es kann ermittelt werden, ob der user doch nicht in der user user_genre_profiles ist
        if target_user_id not in user_genre_profiles:
            #print(f"Error: Target user '{target_user_id}' not found.")
            return []

        #jeden nutzer durchgehen
        for user in users_data:
            #Abfragen ob der momentane Json Block von dem eingeloggten Nutzer ist
            if str(user['name']).lower() == target_user_id:
                #Abfrage ob die List der Favoriten leer ist. Wenn ja soll es nichts zurückgeben und die Listbox nichts anzeigen.
                if user['favorite_movies'] == []:
                    return []

        #Es entimmt das Genre Profil des momentanen Nutzers
        target_user_genres = user_genre_profiles[target_user_id]
        
        #Jeden Nutzer durchgehen
        for user in users_data:
            #Abfrage ob der Json Block von dem Eingeloggten Nutzer ist
            if str(user['name']).lower() == target_user_id:
                # Die Liste der Favoriten des Users auf die Variable speichern für spätere nutzung
                target_user_watched_films = user['favorite_movies']
        
        similarities = []
        #Es überprüft, das der eigentliche Nutzer nicht in der Liste vorhanden ist, bzw ihn überspringt und die For loop bei dem nächsten user anfängt
        for user_id, genres in user_genre_profiles.items():
            if user_id == target_user_id:
                continue #Es gört hier auf und fängt bei dem nächsten User in der List wieder an
            
            #Es überprüft die Ähnlichkeit der Genres des zu prüfenden Nutzers mit den momenanten eingelogten
            sim = self.jaccard_similarity(target_user_genres, genres)

            #Es fügt das Errebnis der Ergebiss liste hinzu mit dem namen des users
            similarities.append((sim, user_id))


        # Die Ähnlichkeiten statistiken in absteigender Folge umsortieren
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Wenn es keine ähnlichkeiten geben sollte, hört das programm hier auf
        if not similarities:
            #print("No other users to compare with.")
            return []

        #Hier wird der User mit den höchsten Ähnlichkeit entnommen werden und der Variable closest_match_user_id hinzugefügt werden
        closest_match_user_id = similarities[0][1]
        
        #Es sollen jetzt die Filme für den Änlichsten User entnommen werden und weiter gegeben werden
        for user in users_data:
            if str(user['name']).lower() == closest_match_user_id:
                closest_match_user_films = user['favorite_movies']
                                                
        #print(closest_match_user_films)
        #Die Ähnlichen filme, die der eingeloggte User nicht hat, der recommended_films Liste hinzufügen
        recommended_films = []
        for film_id in closest_match_user_films:
            if film_id not in target_user_watched_films:
                recommended_films.append(film_id)

        #Die recommended films liste zurück an den controller geben
        return recommended_films