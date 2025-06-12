#----------------------------------------------------Controller
import tkinter as tk # Nur für Typ-Hinting, nicht für UI-Erstellung
from model import Model # Relativer Import, da Model im selben Ordner liegen könnte
from View import View 

class Controler:
    """
    Der Controller verbindet Model und View. Er verarbeitet Benutzeraktionen,
    aktualisiert das Model und weist die View an, sich zu aktualisieren.
    """
    def __init__(self):
        # Initialisiere Model und View
        # Die Pfade zu den JSON-Dateien sollten hier zentral verwaltet werden.
        # Annahme: 'users.json' und 'Films.json' liegen im Unterordner 'data'
        # Passe die Pfade ggf. an deine Dateistruktur an.
        self.model = Model(
            users_filepath=r"Python_Projekt\Ohne_Firebase\users.json",
            films_filepath=r"Python_Projekt\Ohne_Firebase\Films.json"
        )
        # Importiere View hier, um Zirkelabhängigkeiten zu vermeiden, da View den Controller braucht.
        # Alternativ: View-Klassen in separate Dateien auslagern.
        self.view = View(self)
        
        self.current_user = None # Speichert den aktuell eingeloggten Benutzer

        # Startet die Tkinter-Event-Schleife
        self.view.mainloop()

    def handle_login_request(self, username, login_view_instance):
        """
        Verarbeitet die Login-Anfrage vom Login-Fenster.
        """
        if self.model.validate_user(username):
            self.current_user = username.strip()
            login_view_instance.display_login_success(f"Login erfolgreich! Willkommen, {self.current_user}.")
            self.view.after(1000, lambda: self.view.switch_frame(self.view.Main_Window, self.current_user))
        else:
            login_view_instance.display_login_error("Ungültiger Username.")

    def handle_signup_request(self, username, login_view_instance):
        """
        Verarbeitet die Registrierungsanfrage vom Login-Fenster.
        """
        if not username:
            login_view_instance.display_login_error("Username darf nicht leer sein.")
            return

        if self.model.add_new_user(username):
            login_view_instance.display_login_success(f"Registrierung erfolgreich! Bitte logge dich ein.")
            # Normalerweise würde man hier nicht direkt einloggen, sondern den Benutzer bitten, sich einzuloggen.
            # self.current_user = username.strip() 
            # self.view.after(1000, lambda: self.view.switch_frame(self.view.Main_Window, self.current_user))
        else:
            login_view_instance.display_login_error(f"Benutzer '{username}' existiert bereits.")

    def get_all_film_names_for_view(self):
        """
        Holt alle Filmtitel vom Model, um sie in der View anzuzeigen.
        """
        all_films_data = self.model.get_all_films_data()
        return [film.get("name", "Unbekannter Film") for film in all_films_data if film.get("name")]

    def get_recommended_films_for_view(self, username):
        """
        Holt die Lieblingsfilme des Benutzers vom Model und berechnet dann Empfehlungen.
        """
        if not username:
            return []
        liked_movies = self.model.get_user_favorite_movies(username)
        return self.model.get_recommendations(liked_movies)

    def get_user_favorites_for_view(self, username):
        """
        Holt die Lieblingsfilme eines Benutzers vom Model, um sie im Favoritenfenster anzuzeigen.
        """
        return self.model.get_user_favorite_movies(username)

    def handle_film_search(self, search_term, main_window_instance):
        """
        Führt die Filmsuche durch und aktualisiert die Filmliste in der Main_Window View.
        """
        all_films_data = self.model.get_all_films_data()
        filtered_films_names = []
        if search_term:
            for film in all_films_data:
                film_name = film.get("name", "").lower()
                film_description = film.get("description", "").lower() # Annahme: Beschreibung existiert
                if search_term.lower() in film_name or search_term.lower() in film_description:
                    filtered_films_names.append(film.get("name"))
        else:
            filtered_films_names = self.get_all_film_names_for_view()
        
        main_window_instance.update_available_films_list(filtered_films_names)

    def add_to_favorites(self, film_title):
        """
        (Platzhalter) Fügt einen Film zu den Favoriten des aktuellen Benutzers hinzu.
        Diese Logik müsste im Model implementiert und hier aufgerufen werden.
        """
        # Beispiel: Hier würde man dem Model mitteilen, den Film zu den Favoriten hinzuzufügen
        # self.model.add_favorite_movie(self.current_user, film_title)
        self.view.display_message(f"'{film_title}' wurde zu Favoriten hinzugefügt (Funktionalität noch zu implementieren).")