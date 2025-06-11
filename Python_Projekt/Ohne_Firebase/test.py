import tkinter as tk
from tkinter import messagebox
from collections import Counter

# --- Model (MovieModel.py) ---
class MovieModel:
    """
    Das Model verwaltet die Filmdaten und die Empfehlungslogik.
    Es speichert alle verfügbaren Filme, die vom Benutzer gemochten Filme
    und generiert Empfehlungen basierend auf inhaltsbasierter Filterung (Genres).
    """
    def __init__(self):
        # Beispiel-Filmdaten mit Titel und Genres
        # In einer echten Anwendung würden diese Daten aus einer Datenbank oder API geladen
        self.movies_data = [
            {"title": "Die Matrix", "genres": ["Action"]},
            {"title": "Inception", "genres": ["Action"]},
            {"title": "Interstellar", "genres": ["Sci-Fi"]},
            {"title": "Der Herr der Ringe: Die Gefährten", "genres": ["Fantasy", "Adventure"]},
            {"title": "Guardians of the Galaxy", "genres": ["Sci-Fi"]},
            {"title": "Die Verurteilten", "genres": ["Drama"]},
            {"title": "Forrest Gump", "genres": ["Drama", "Romance"]},
            {"title": "Pulp Fiction", "genres": ["Crime", "Drama"]},
            {"title": "Titanic", "genres": ["Romance", "Drama"]},
            {"title": "Yvatar", "genres": ["Action"]},
            {"title": "Dune", "genres": ["Sci-Fi", "Adventure", "Drama"]},
            {"title": "Blade Runner 2049", "genres": ["Sci-Fi", "Drama", "Mystery"]},
            {"title": "Arrival", "genres": ["Sci-Fi", "Drama", "Mystery"]},
            {"title": "Der König der Löwen", "genres": ["Animation", "Family", "Musical"]},
            {"title": "Toy Story", "genres": ["Animation", "Family", "Comedy"]},
            {"title": "Schindlers Liste", "genres": ["Drama", "History", "War"]},
            {"title": "Der Pate", "genres": ["Crime", "Drama"]},
            {"title": "Fight Club", "genres": ["Drama", "Thriller"]},
            {"title": "Ewiger Sonnenschein des makellosen Geistes", "genres": ["Romance", "Sci-Fi", "Drama"]}
        ]
        # Liste der Titel der Filme, die der Benutzer mag
        self.liked_movie_titles = []

    def get_all_movie_titles(self):
        """Gibt eine Liste aller Filmtitel zurück."""
        return [movie["title"] for movie in self.movies_data]

    def add_liked_movie(self, movie_title):
        """
        Fügt einen Film zur Liste der gemochten Filme hinzu, falls er noch nicht vorhanden ist.
        """
        if movie_title not in self.liked_movie_titles:
            self.liked_movie_titles.append(movie_title)
            return True
        return False

    def get_liked_movie_titles(self):
        """Gibt die Liste der gemochten Filmtitel zurück."""
        return self.liked_movie_titles

    def get_recommendations(self):
        """
        Generiert Filmempfehlungen basierend auf den Genres der gemochten Filme.
        Verwendet eine einfache inhaltsbasierte Filterung.
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

# --- View (MovieView.py) ---
class MovieView(tk.Frame):
    """
    Die View ist für die Darstellung der Benutzeroberfläche zuständig.
    Sie enthält alle Tkinter-Widgets und zeigt die Filmlisten an.
    Sie hat keine direkte Logik, sondern informiert den Controller über Benutzerinteraktionen.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Filmempfehlungssystem")
        self.controller = None # Wird später vom Controller gesetzt
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_widgets()

    def set_controller(self, controller):
        """Setzt die Referenz zum Controller und bindet die Button-Befehle."""
        self.controller = controller
        # Setzt die Befehle für die Buttons, nachdem der Controller verfügbar ist
        self.add_button.config(command=self.controller.add_movie)
        self.recommend_button.config(command=self.controller.show_recommendations)

    def create_widgets(self):
        """Erstellt alle GUI-Widgets."""
        # Frame für verfügbare Filme
        available_movies_frame = tk.LabelFrame(self, text="Verfügbare Filme")
        available_movies_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.available_movies_listbox = tk.Listbox(available_movies_frame, height=15, selectmode=tk.SINGLE)
        self.available_movies_listbox.pack(fill=tk.BOTH, expand=True)
        available_movies_scrollbar = tk.Scrollbar(available_movies_frame, orient="vertical", command=self.available_movies_listbox.yview)
        available_movies_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.available_movies_listbox.config(yscrollcommand=available_movies_scrollbar.set)

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.LEFT, padx=10)

        # Speichern Sie die Button-Referenzen, um ihre Befehle später zu konfigurieren
        self.add_button = tk.Button(button_frame, text=">>> Film hinzufügen >>>")
        self.add_button.pack(pady=5)

        self.recommend_button = tk.Button(button_frame, text="Empfehlungen anzeigen")
        self.recommend_button.pack(pady=5)

        # Frame für gemochte Filme
        liked_movies_frame = tk.LabelFrame(self, text="Interessierte Filme")
        liked_movies_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.liked_movies_listbox = tk.Listbox(liked_movies_frame, height=15)
        self.liked_movies_listbox.pack(fill=tk.BOTH, expand=True)
        liked_movies_scrollbar = tk.Scrollbar(liked_movies_frame, orient="vertical", command=self.liked_movies_listbox.yview)
        liked_movies_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.liked_movies_listbox.config(yscrollcommand=liked_movies_scrollbar.set)

        # Frame für empfohlene Filme
        recommended_movies_frame = tk.LabelFrame(self, text="Empfohlene Filme")
        recommended_movies_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.recommended_movies_listbox = tk.Listbox(recommended_movies_frame, height=15)
        self.recommended_movies_listbox.pack(fill=tk.BOTH, expand=True)
        recommended_movies_scrollbar = tk.Scrollbar(recommended_movies_frame, orient="vertical", command=self.recommended_movies_listbox.yview)
        recommended_movies_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.recommended_movies_listbox.config(yscrollcommand=recommended_movies_scrollbar.set)

    def update_movie_lists(self, all_movies, liked_movies, recommended_movies):
        """
        Aktualisiert die Anzeigelisten in der GUI.
        """
        # Verfügbare Filme aktualisieren
        self.available_movies_listbox.delete(0, tk.END)
        for movie in all_movies:
            self.available_movies_listbox.insert(tk.END, movie)
        
        # Gemochte Filme aktualisieren
        self.liked_movies_listbox.delete(0, tk.END)
        for movie in liked_movies:
            self.liked_movies_listbox.insert(tk.END, movie)

        # Empfohlene Filme aktualisieren
        self.recommended_movies_listbox.delete(0, tk.END)
        for movie in recommended_movies:
            self.recommended_movies_listbox.insert(tk.END, movie)

    def get_selected_movie(self):
        """Gibt den Titel des aktuell ausgewählten Films in der Liste der verfügbaren Filme zurück."""
        selected_indices = self.available_movies_listbox.curselection()
        if selected_indices:
            return self.available_movies_listbox.get(selected_indices[0])
        return None

    def show_info_message(self, title, message):
        """Zeigt eine Informationsnachricht an."""
        messagebox.showinfo(title, message)

    def show_warning_message(self, title, message):
        """Zeigt eine Warnmeldung an."""
        messagebox.showwarning(title, message)


# --- Controller (MovieController.py) ---
class MovieController:
    """
    Der Controller fungiert als Vermittler zwischen Model und View.
    Er verarbeitet Benutzeraktionen von der View, aktualisiert das Model
    und weist die View an, sich entsprechend zu aktualisieren.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self) # Setzt den Controller in der View
        
        # Initialisiere die Listen in der View
        self._update_all_lists()

    def _update_all_lists(self):
        """Hilfsfunktion zum Aktualisieren aller Listen in der View."""
        all_movies = self.model.get_all_movie_titles()
        liked_movies = self.model.get_liked_movie_titles()
        # Empfehlungen werden nicht standardmäßig aktualisiert, nur auf Klick
        recommended_movies = [] 
        self.view.update_movie_lists(all_movies, liked_movies, recommended_movies)

    def add_movie(self):
        """
        Wird aufgerufen, wenn der Benutzer auf 'Film hinzufügen' klickt.
        Holt den ausgewählten Film, fügt ihn zum Model hinzu und aktualisiert die View.
        """
        selected_movie = self.view.get_selected_movie()
        if selected_movie:
            if self.model.add_liked_movie(selected_movie):
                self.view.show_info_message("Film hinzugefügt", f"'{selected_movie}' wurde zu Ihren interessierten Filmen hinzugefügt.")
                self._update_all_lists() # Aktualisiere alle Listen nach dem Hinzufügen
            else:
                self.view.show_warning_message("Bereits hinzugefügt", f"'{selected_movie}' ist bereits in Ihrer Liste der interessierten Filme.")
        else:
            self.view.show_warning_message("Keine Auswahl", "Bitte wählen Sie einen Film aus der Liste 'Verfügbare Filme' aus.")

    def show_recommendations(self):
        """
        Wird aufgerufen, wenn der Benutzer auf 'Empfehlungen anzeigen' klickt.
        Holt Empfehlungen vom Model und aktualisiert die View.
        """
        recommended_movies = self.model.get_recommendations()
        all_movies = self.model.get_all_movie_titles() # Brauchen wir, um die verfügbaren Filme neu zu laden
        liked_movies = self.model.get_liked_movie_titles() # Brauchen wir, um die gemochten Filme neu zu laden

        self.view.update_movie_lists(all_movies, liked_movies, recommended_movies)

        if not recommended_movies:
            self.view.show_info_message("Keine Empfehlungen", "Basierend auf Ihren Präferenzen konnten keine neuen Filmempfehlungen gefunden werden. Fügen Sie weitere Filme zu 'Interessierte Filme' hinzu.")

    def start(self):
        """Startet die Tkinter-Hauptschleife."""
        self.view.mainloop()

# --- Hauptprogramm ---
if __name__ == "__main__":
    root = tk.Tk()
    
    # MVC-Instanzen erstellen
    model = MovieModel()
    view = MovieView(master=root)
    controller = MovieController(model, view)

    # Starten der Anwendung
    controller.start()