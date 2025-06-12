#-----------------------------------------------------View
import tkinter as tk
from tkinter import messagebox # Für benutzerfreundliche Meldungen statt print

class View(tk.Tk):
    """
    Die View ist die grafische Benutzeroberfläche der Anwendung.
    Sie zeigt Daten an und erfasst Benutzerinteraktionen, leitet diese aber
    an den Controller weiter. Sie hat keine Anwendungslogik selbst.
    """
    def __init__(self, controller):
        super().__init__()
        self.geometry("800x600")
        self.title("Film Vorschlags Applikation")
        self.controller = controller
        self._frame = None
        self.current_message_label = None # Zum Anzeigen von Fehlermeldungen

        # Starte mit dem Login-Fenster
        self.switch_frame(self.Login_Window)

    def switch_frame(self, frame_class, user=None):
        """
        Wechselt das aktuell angezeigte Frame.
        """
        if self._frame is not None:
            self._frame.destroy()
        
        # Jedes Frame benötigt den Controller und ggf. den Benutzer
        new_frame = frame_class(self, self.controller, user)
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=True) # Füllt das gesamte Fenster

    def display_message(self, message, is_error=False):
        """Zeigt eine Nachricht (oder Fehlermeldung) im UI an."""
        if self.current_message_label:
            self.current_message_label.destroy() # Alte Nachricht entfernen

        # Erstelle ein neues Label für die Nachricht
        self.current_message_label = tk.Label(self, text=message, fg="red" if is_error else "blue")
        self.current_message_label.pack(pady=5)
        self.after(5000, self.clear_message) # Nachricht nach 5 Sekunden entfernen

    def clear_message(self):
        """Entfernt die aktuell angezeigte Nachricht."""
        if self.current_message_label:
            self.current_message_label.destroy()
            self.current_message_label = None

    class Login_Window(tk.Frame):
        """
        Das Login-Fenster zur Benutzeranmeldung oder -registrierung.
        """
        def __init__(self, master, controller, user_data=None):
            super().__init__(master)
            self.master = master
            self.controller = controller

            # Login-Bereich
            tk.Label(self, text="Einloggen", font=("Arial", 16, "bold")).pack(pady=10)
            tk.Label(self, text="Username:").pack(pady=2)
            self.login_Entry = tk.Entry(self, width=30, font=("Arial", 12))
            self.login_Entry.pack(pady=5)
            tk.Button(self, text="Login", command=self._on_login, font=("Arial", 12)).pack(pady=10)

            # Signup-Bereich
            tk.Label(self, text="Registrieren", font=("Arial", 16, "bold")).pack(pady=20)
            tk.Label(self, text="Neuer Username:").pack(pady=2)
            self.signup_Entry = tk.Entry(self, width=30, font=("Arial", 12))
            self.signup_Entry.pack(pady=5)
            tk.Button(self, text="Registrieren", command=self._on_signup, font=("Arial", 12)).pack(pady=10)

            self.message_label = tk.Label(self, text="", fg="red")
            self.message_label.pack(pady=5)

        def _on_login(self):
            """Wird aufgerufen, wenn der Login-Button geklickt wird."""
            username = self.login_Entry.get().strip()
            self.controller.handle_login_request(username, self)

        def _on_signup(self):
            """Wird aufgerufen, wenn der Registrieren-Button geklickt wird."""
            username = self.signup_Entry.get().strip()
            self.controller.handle_signup_request(username, self)

        def display_login_error(self, message):
            """Zeigt eine Fehlermeldung im Login-Fenster an."""
            self.message_label.config(text=message, fg="red")
            self.master.after(3000, lambda: self.message_label.config(text="")) # Nachricht nach 3s entfernen

        def display_login_success(self, message):
            """Zeigt eine Erfolgsmeldung im Login-Fenster an."""
            self.message_label.config(text=message, fg="green")
            self.master.after(3000, lambda: self.message_label.config(text="")) # Nachricht nach 3s entfernen

    class Main_Window(tk.Frame):
        """
        Das Hauptfenster der Anwendung, zeigt verfügbare und empfohlene Filme an.
        """
        def __init__(self, master, controller, user):
            super().__init__(master)
            self.master = master
            self.controller = controller
            self.current_user = user # Der aktuell eingeloggte Benutzer
            self.all_available_films = [] # Wird vom Controller gefüllt
            self.current_film_filter_term = "" # Für die Suchfunktion

            self.grid_rowconfigure(3, weight=1) # Row for listboxes
            self.grid_columnconfigure(0, weight=1) # Column for left listbox
            self.grid_columnconfigure(1, weight=1) # Column for right listbox

            tk.Label(self, text=f"Willkommen, {self.current_user}!", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
            
            tk.Button(self, text="Meine Favoriten", command=self._on_favorites_click, font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=5)

            # --- Linke Sektion: Verfügbare Filme ---
            tk.Label(self, text="Verfügbare Filme:", font=("Arial", 14, "bold")).grid(row=2, column=0, sticky=tk.SW, padx=5, pady=5)

            self.film_listbox_frame = tk.Frame(self, bd=2, relief="groove")
            self.film_listbox_frame.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_frame.grid_rowconfigure(2, weight=1) # Listbox row
            self.film_listbox_frame.grid_columnconfigure(0, weight=1)

            tk.Label(self.film_listbox_frame, text="Film suchen:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            self.search_entry = tk.Entry(self.film_listbox_frame, width=40, font=("Arial", 10))
            self.search_entry.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=2)
            self.search_entry.bind("<KeyRelease>", self._on_search_key_release)

            self.clear_search_button = tk.Button(self.film_listbox_frame, text="Suche zurücksetzen", command=self._on_clear_search, font=("Arial", 10))
            self.clear_search_button.grid(row=1, column=1, sticky=tk.E, padx=5, pady=2) # Changed to column 1

            self.film_listbox_scrollbar = tk.Scrollbar(self.film_listbox_frame)
            self.film_listbox_scrollbar.grid(row=2, column=1, sticky=tk.NS)

            self.film_listbox = tk.Listbox(self.film_listbox_frame,
                                           height=15,
                                           yscrollcommand=self.film_listbox_scrollbar.set,
                                           font=("Arial", 12),
                                           selectmode=tk.SINGLE)
            self.film_listbox.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_scrollbar.config(command=self.film_listbox.yview)

            # --- Rechte Sektion: Empfohlene Filme ---
            tk.Label(self, text="Empfohlene Filme:", font=("Arial", 14, "bold")).grid(row=2, column=1, sticky=tk.SW, padx=5, pady=5)

            self.recommended_listbox_frame = tk.Frame(self, bd=2, relief="groove")
            self.recommended_listbox_frame.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=1)
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                 height=15,
                                                 yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                 font=("Arial", 12))
            self.recommended_listbox.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)
            
            # Initialisiere die Listen über den Controller
            self.update_available_films_list()
            self.update_recommended_films_list()

        def _on_favorites_click(self):
            """Wechselt zum Favoritenfenster."""
            self.master.switch_frame(self.master.Favorites_Window, self.current_user)

        def _on_search_key_release(self, event=None):
            """Filtert die Filmliste basierend auf der Sucheingabe."""
            self.current_film_filter_term = self.search_entry.get().strip()
            # Hier ruft die View den Controller auf, um die Filterung zu initiieren
            self.controller.handle_film_search(self.current_film_filter_term, self)

        def _on_clear_search(self):
            """Setzt die Suche zurück und zeigt alle Filme an."""
            self.search_entry.delete(0, tk.END)
            self.current_film_filter_term = ""
            self.update_available_films_list() # Alle Filme erneut laden

        def update_available_films_list(self, films_to_display=None):
            """
            Aktualisiert die Liste der verfügbaren Filme.
            Kann entweder eine gefilterte Liste oder alle Filme vom Controller erhalten.
            """
            self.film_listbox.delete(0, tk.END)
            if films_to_display is None:
                films_to_display = self.controller.get_all_film_names_for_view()
            
            for film_name in films_to_display:
                self.film_listbox.insert(tk.END, film_name)
        
        def update_recommended_films_list(self):
            """
            Aktualisiert die Liste der empfohlenen Filme.
            """
            self.recommended_listbox.delete(0, tk.END)
            recommended_films = self.controller.get_recommended_films_for_view(self.current_user)
            for film_name in recommended_films:
                self.recommended_listbox.insert(tk.END, film_name)

    class Film_Kachel(tk.Frame):
        """
        Eine Beispiel-Film-Kachel (derzeit nicht vollständig implementiert, aber hier als Platzhalter für MVC-Struktur).
        """
        def __init__(self, master, controller, film_data):
            super().__init__(master)
            self.controller = controller
            self.film_data = film_data

            tk.Label(self, text=film_data.get("name", "N/A"), font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=2)
            tk.Label(self, text=film_data.get("description", "Keine Beschreibung."), font=("Arial", 10), wraplength=200).grid(row=1, column=0, padx=5, pady=2)
            tk.Button(self, text="Zu Favoriten hinzufügen", command=lambda: self.controller.add_to_favorites(self.film_data["name"]), font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)


    class Favorites_Window(tk.Frame):
        """
        Fenster zum Anzeigen der Lieblingsfilme des Benutzers.
        """
        def __init__(self, master, controller, user):
            super().__init__(master)
            self.master = master
            self.controller = controller
            self.current_user = user

            tk.Label(self, text=f"Deine Lieblingsfilme, {self.current_user}", font=("Arial", 18, "bold")).pack(pady=10)
            
            tk.Button(self, text="Zurück zum Hauptfenster", command=self._on_main_window_click, font=("Arial", 12)).pack(pady=5)

            tk.Label(self, text="Deine Favoriten:", font=("Arial", 14, "bold")).pack(pady=5)

            self.favorites_listbox_frame = tk.Frame(self, bd=2, relief="groove")
            self.favorites_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            self.favorites_listbox_frame.grid_rowconfigure(0, weight=1)
            self.favorites_listbox_frame.grid_columnconfigure(0, weight=1)

            self.favorites_listbox_scrollbar = tk.Scrollbar(self.favorites_listbox_frame)
            self.favorites_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.favorites_listbox = tk.Listbox(self.favorites_listbox_frame,
                                                 height=15,
                                                 yscrollcommand=self.favorites_listbox_scrollbar.set,
                                                 font=("Arial", 12))
            self.favorites_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.favorites_listbox_scrollbar.config(command=self.favorites_listbox.yview)

            self.update_favorites_list()

        def _on_main_window_click(self):
            """Wechselt zurück zum Hauptfenster."""
            self.master.switch_frame(self.master.Main_Window, self.current_user)

        def update_favorites_list(self):
            """Aktualisiert die Liste der Lieblingsfilme."""
            self.favorites_listbox.delete(0, tk.END)
            favorite_films = self.controller.get_user_favorites_for_view(self.current_user)
            for film_name in favorite_films:
                self.favorites_listbox.insert(tk.END, film_name)