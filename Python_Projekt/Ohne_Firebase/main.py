import tkinter as tk
import sys
import json
from collections import Counter

#----------------------------------------------------Model
class Model():
    
    def load(file):
        try:
            with open(file) as in_file:
                loaded_txt = in_file.read().lower().strip("").split('\n')
                    
                return loaded_txt
            
        except IOError as e:
            print("{}\nError opening {}. Terminating program.".format(e, file),
                file=sys.stderr)
            sys.exit(1)

    def get_recommended_films_from_json(self, filepath, user):
        favorite_movies_names = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
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
            print(f"Fehler: Datei nicht gefunden unter: {filepath}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        print(favorite_movies_names)
        recommdenations = self.get_recommendations(favorite_movies_names)
        
        return recommdenations

    def get_names_from_json(self, filepath):
        names = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
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
            print(f"Fehler: Datei nicht gefunden unter: {filepath}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return names


    def get_films_from_json(self, filepath):
        films = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
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
            print(f"Fehler: Datei nicht gefunden unter: {filepath}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return films
    
    def get_json(self, filepath):
        films = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden unter: {filepath}")
        except json.JSONDecodeError:
            print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        return data
    
    def get_recommendations(self, liked_movie_titles):
        if not liked_movie_titles:
            return [] # Keine Empfehlungen, wenn keine Filme gemocht werden

        # Sammle alle Genres der gemochten Filme
        liked_genres = []
        for liked_title in liked_movie_titles:
            for movie in self.get_json(r"Python_Projekt\Ohne_Firebase\Films.json"):
                #print(movie["name"])
                #print(liked_title)
                if str(movie["name"]).strip().lower() == str(liked_title).strip():
                    liked_genres.extend(movie["genre"])
                    break
        
        # Zähle die Häufigkeit der Genres, um Präferenzen zu ermitteln
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        recommended_films = []
        for movie in self.get_json(r"Python_Projekt\Ohne_Firebase\Films.json"):
            movie_title = movie["name"]
            # Empfehle keine Filme, die bereits gemocht werden
            if movie_title in liked_movie_titles:
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
        print(recommended_films)
        return recommended_films

#-----------------------------------------------------View
class View(tk.Tk):
    def __init__(self,controler):
        super().__init__()
        #Window erstellen mit der 800 pixel breite und 600 pixel höhe, sowie dem namen Film Vorschlags Applikation 
        self.geometry("800x600")
        self.title("Film Vorschlags Applikation")
        self.controller = controler
        self._frame = None
        self.switch_frame(self.Login_Window, controler, None)
        

    def switch_frame(self, frame_class, controler, user):
        new_frame = frame_class(self, controler, user)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    

    class Login_Window(tk.Frame):
        def __init__(self, master, controler, user):
            super().__init__(master)
            self.master = master
            self.login_Label = tk.Label(self, text = "Einloggen")
            self.login_Label.pack()
            self.login_Entry = tk.Entry(self, text = "Username")
            self.login_Entry.pack()
            self.login_button = tk.Button(self, text= "Login", command = lambda : (controler.login(self.login_Entry, self.master)))
            self.login_button.pack()
            self.signup_label = tk.Label(self, text = "Signup")
            self.signup_label.pack()
            self.signup_Entry = tk.Entry(self, text = "SignUp")
            self.signup_Entry.pack()
            self.signup_button = tk.Button(self, text = "Signup", command = lambda : (self.signup(controler)))
            self.signup_button.pack()
            

        def signup(self, controler):
            #User muss noch der Datei beigefügt werden und nanch erfolgreichem Signup weiterleiten
            users = controler.get_Json_User_Names()
            for user_ls in users:
                user = self.signup_Entry.get()
                user = user.strip().lower()
                print(user)
                print(str(user_ls))

                if user != str(user_ls).strip():
                    pass
                    #self.master.switch_frame(Main_Window)
                
                else:
                    print("Es gibt den user")

    class Main_Window(tk.Frame):
        def __init__(self, master, controler, user):
            super().__init__(master)
            self.recomended_films = None
            self.controler = controler

            # Configure grid to expand with window
            self.grid_rowconfigure(2, weight=1) # Row for listboxes
            self.grid_columnconfigure(0, weight=1) # Column for left listbox
            self.grid_columnconfigure(1, weight=1) # Column for right listbox

            self.Label = tk.Label(self, text="Mainwframe")
            self.Label.grid(row=0, column=0, columnspan=2, pady=5) # Spans both columns

            self.Button = tk.Button(self, text="Favorites", command=lambda: master.switch_frame(master.Favorites_Window, controler, user))
            self.Button.grid(row=1, column=0, columnspan=2, pady=5) # Spans both columns

            # --- Left Listbox (Available Films) ---
            
            self.film_listbox_label = tk.Label(self, text="Available Films:")
            self.film_listbox_label.grid(row=2, column=0, sticky=tk.SW, padx=5, pady=2) # sticky=tk.SW aligns to bottom-left

            self.film_listbox_frame = tk.Frame(self) # Create a frame to hold listbox and scrollbar
            self.film_listbox_frame.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_frame.grid_rowconfigure(0, weight=1)
            self.film_listbox_frame.grid_columnconfigure(0, weight=1)

            self.search_label = tk.Label(self.film_listbox_frame, text="Search Film:")
            self.search_label.grid()

            self.search_entry = tk.Entry(self.film_listbox_frame, width=40)
            self.search_entry.grid()
            self.search_entry.bind("<KeyRelease>", self.filter_films) # Live search

            self.clear_search_button = tk.Button(self.film_listbox_frame, text="Clear", command=self.clear_search)
            self.clear_search_button.grid()

            self.film_listbox_scrollbar = tk.Scrollbar(self.film_listbox_frame)
            self.film_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.film_listbox = tk.Listbox(self.film_listbox_frame,
                                            height=15,
                                            yscrollcommand=self.film_listbox_scrollbar.set,
                                            font=("Arial", 12))
            self.film_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.film_listbox_scrollbar.config(command=self.film_listbox.yview)

            # --- Right Listbox (Recommended Films) ---
            self.recommended_listbox_label = tk.Label(self, text="Recommended Films:") # Changed label text
            self.recommended_listbox_label.grid(row=2, column=1, sticky=tk.SW, padx=5, pady=2) # sticky=tk.SW aligns to bottom-left

            self.recommended_listbox_frame = tk.Frame(self) # Create a frame to hold listbox and scrollbar
            self.recommended_listbox_frame.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=1)
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                font=("Arial", 12))
            self.recommended_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)

            self.list_Films(self.controler.get_Json_Film_Names())
            self.list_recommended_Films(user)

        def clear_search(self):
            films = self.controler.get_Json_Film_Names()
            self.search_entry.delete(0, tk.END)
            self.film_listbox(films)
            self.clear_film_details()

        def filter_films(self, event = None):
            search_term = self.search_entry.get().lower()
            films = self.controler.get_Json_Film_Names()
            filtered_films = []
            for film in films:
                if search_term in film.lower():
                    filtered_films.append(film)

            print(filtered_films)   
            self.list_Films(filtered_films)
            

        """def on_film_select(self, event):
            selected_indices = self.film_listbox.curselection()
            if not selected_indices:
                self.clear_film_details()
                return

            index = selected_indices[0]
            selected_film_name = self.film_listbox.get(index)

            selected_film_data = next((film for film in self.films if film["name"] == selected_film_name), None)

            if selected_film_data:
                self.film_name_label.config(text=f"Name: {selected_film_data['name']}")
                self.film_description_label.config(text=f"Description: {selected_film_data['description']}")
                self.trailer_button.config(state=tk.NORMAL)
                self.current_selected_film = selected_film_data # Store for button action
            else:
                self.clear_film_details()"""

        def list_Films(self, films):
            self.film_listbox.delete(0, tk.END) # Clear existing items
            for film in films:
                self.film_listbox.insert(tk.END, film)
        
        def list_recommended_Films(self, user):
            self.recommended_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_recommended_Film_Names(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)
        
    class Film_Kachel(tk.Frame):
            def __init__(self,master, Film):
                super().__init__(master)
                Film_Name = tk.Label(self, text = Film)
                Film_Name.grid(row=0, column=0)
                Film_beschreibung = tk.Label(self, text= Film[1])
                Film_beschreibung.grid(row=0, column=1)
                button = tk.Button(self, text = "Add to favroites")
                button.grid(row=0, column=2)

    class Favorites_Window(tk.Frame):
        def __init__(self, master,controler, user):
            super().__init__(master)
            self.controler = controler

            self.Label = tk.Label(self, text = "Favorites")
            self.Label.grid()

            self.Button = tk.Button(self, text = "Main Window", command = lambda : master.switch_frame(master.Main_Window, controler, user))
            self.Button.grid()

            self.recommended_listbox_label = tk.Label(self, text="Recommended Films:") # Changed label text
            self.recommended_listbox_label.grid(row=2, column=1, sticky=tk.SW, padx=5, pady=2) # sticky=tk.SW aligns to bottom-left

            self.recommended_listbox_frame = tk.Frame(self) # Create a frame to hold listbox and scrollbar
            self.recommended_listbox_frame.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=1)
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                font=("Arial", 12))
            self.recommended_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)

            self.List_Produkts(user)

        
        def List_Produkts(self, user):
            self.recommended_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_recommended_Film_Names(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)

class Controler():
    def __init__(self):
        self.model = Model()
        self.view = View(self)

        self.view.mainloop()
    
    def login(self, login_Entry, master):
        users = self.get_Json_User_Names()
        for user_ls in users:
            user = login_Entry.get()
            user = user.strip()
            print(user)
            print(str(user_ls))

            if user == str(user_ls).strip():
                master.switch_frame(master.Main_Window, self, user)
                break
            
            else:
                print("Es gibt den User nicht")

    def get_Json_Film_Names(self):
        Film_names = self.model.get_films_from_json(r"Python_Projekt\Ohne_Firebase\Films.json")
        return Film_names

    def get_Json_User_Names(self):
        Film_names = self.model.get_names_from_json(r"Python_Projekt\Ohne_Firebase\users.json")
        return Film_names
    
    def get_Json_recommended_Film_Names(self, user):
        Film_names = self.model.get_recommended_films_from_json(r"Python_Projekt\Ohne_Firebase\users.json", user)
        print(Film_names)
        return Film_names

if __name__ == "__main__":
    controler = Controler()
    