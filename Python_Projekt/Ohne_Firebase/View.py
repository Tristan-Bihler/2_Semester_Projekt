import tkinter as tk
import Filehandler as Fh

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        #Window erstellen mit der 800 pixel breite und 600 pixel höhe, sowie dem namen Film Vorschlags Applikation 
        self.geometry("800x600")
        self.title("Film Vorschlags Applikation")
        self.controller = None
        self._frame = None
        self.switch_frame(Login_Window)
        self.mainloop()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    

class Login_Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.login_Label = tk.Label(self, text = "Einloggen")
        self.login_Label.pack()
        self.login_Entry = tk.Entry(self, text = "Username")
        self.login_Entry.pack()
        self.login_button = tk.Button(self, text= "Login", command = self.login)
        self.login_button.pack()
        self.signup_label = tk.Label(self, text = "Signup")
        self.signup_label.pack()
        self.signup_Entry = tk.Entry(self, text = "SignUp")
        self.signup_Entry.pack()
        self.signup_button = tk.Button(self, text = "Signup", command = self.signup)
        self.signup_button.pack()
    
    def login(self):
        users = Fh.get_names_from_json(r"Python_Projekt\Ohne_Firebase\users.json")
        for user_ls in users:
            user = self.login_Entry.get()
            user = user.strip().lower()
            print(user)
            print(str(user_ls))

            if user == str(user_ls).strip():
                self.master.switch_frame(Main_Window)
                break
            
            else:
                print("Es gibt den User nicht")

    def signup(self):
        #User muss noch der Datei beigefügt werden und nanch erfolgreichem Signup weiterleiten
        users = Fh.get_names_from_json(r"Python_Projekt\Ohne_Firebase\users.json")
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
    def __init__(self, master):
        super().__init__(master)

        self.recomended_films = None


        self.Label = tk.Label(self, text="Mainwframe")
        self.Label.pack()
        self.Button = tk.Button(self, text="Favorites", command= lambda : master.switch_frame(Favorites_Window))
        self.Button.pack()
        
        self.canvas = tk.Canvas(self, borderwidth=0)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.films_frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.films_frame, anchor="nw")

        self.films_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.list_Produkts()


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def list_Films(self):
        #print(Films)
        Film_names = Fh.get_films_from_json(r"Python_Projekt\Ohne_Firebase\Films.json")
        for Film_name in Film_names:
            Film_kachel_instance = Film_Kachel(self.films_frame, Film_name)
            Film_kachel_instance.pack()
            #print(Film[0])
    
    def list_recommended_Films(self):
        #print(Films)
        #Hier muss der Algorythmus rein
        Film_names = self.recomended_films
        for Film_name in Film_names:
            Film_kachel_instance = Film_Kachel(self.films_frame, Film_name)
            Film_kachel_instance.pack()
            #print(Film[0])
    
    def get_recommendations(self):
        """
        if not self.liked_movie_titles:
            return [] # Keine Empfehlungen, wenn keine Filme gemocht werden

        # Sammle alle Genres der gemochten Filme
        liked_genres = []
        for liked_title in self.liked_movie_titles:
            for movie in self.movies_data:
                if movie["title"] == liked_title:
                    liked_genres.extend(movie["genres"])
                    break
        
        # Zähle die Häufigkeit der Genres, um Präferenzen zu ermitteln
        genre_counts = Counter(liked_genres)

        recommendations_with_scores = {}
        for movie in self.movies_data:
            movie_title = movie["title"]
            # Empfehle keine Filme, die bereits gemocht werden
            if movie_title in self.liked_movie_titles:
                continue

            score = 0
            # Berechne einen Score basierend auf übereinstimmenden Genres und deren Häufigkeit
            for genre in movie["genres"]:
                score += genre_counts.get(genre, 0) # Addiere die Häufigkeit des Genres

            if score > 0: # Nur Filme mit mindestens einer Genre-Übereinstimmung hinzufügen
                recommendations_with_scores[movie_title] = score
        
        # Sortiere Empfehlungen nach Score (absteigend)
        sorted_recommendations = sorted(recommendations_with_scores.items(), key=lambda item: item[1], reverse=True)
        
        return [title for title, score in sorted_recommendations]
        """

class Film_Kachel(tk.Frame):
        def __init__(self,master, Film):
            super().__init__(master)
            Film_Name = tk.Label(self, text = Film)
            Film_Name.grid(row=0, column=0)
            Film_beschreibung = tk.Label(self, text= Film[1])
            Film_beschreibung.grid(row=0, column=1)
            button = tk.Button(self, text = "Add to favroites")
            button.grid(row=0, column=2)

class Liked_Film_Kachel(tk.Frame):
        def __init__(self,master, Film):
            super().__init__(master)
            Film_Name = tk.Label(self, text = Film[0])
            Film_Name.grid(row=0, column=0)
            Film_beschreibung = tk.Label(self, text= Film[1])
            Film_beschreibung.grid(row=0, column=1)
            button = tk.Button(self, text = "Remove from Favorites")
            button.grid(row=0, column=2)

class Favorites_Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Label = tk.Label(self, text = "Favorites")
        self.Label.pack()

        self.Button = tk.Button(self, text = "Main Window", command = lambda : master.switch_frame(Main_Window))
        self.Button.pack()

        self.canvas = tk.Canvas(self, borderwidth=0)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.films_frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.films_frame, anchor="nw")

        self.films_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.List_Produkts()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def List_Produkts(self):
        pass
        #Films = Fh.load(r"Python_Projekt\Ohne_Firebase\Films.txt")
        #print(Films)
        #for Film in Films:
        #    Film = Film.split(",")
        #    Film_kachel_instance = Liked_Film_Kachel(self.films_frame, Film)
        #    Film_kachel_instance.pack()
        #    #print(Film[0])
