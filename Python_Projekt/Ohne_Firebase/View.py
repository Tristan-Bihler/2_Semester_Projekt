import tkinter as tk
import webbrowser
#-----------------------------------------------------View
class View(tk.Tk):
    def __init__(self,controler):
        super().__init__()
        #Window erstellen mit der 800 pixel breite und 600 pixel höhe, sowie dem namen Film Vorschlags Applikation 
        self.geometry("1000x800")
        self.title("Film Vorschlags Applikation")
        self.controller = controler
        #Wechseln in das Login Fenster
        self._frame = None
        self.switch_frame(self.Login_Window, controler, None)
        
    #Die Wechselfunktion für das Wechseln verschiedener ansichts Bereiche
    def switch_frame(self, frame_class, controler, user):
        new_frame = frame_class(self, controler, user)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
    """
    Die Visuelle übersicht für das Login fenster mit verschiedenen Elementen
    Der Loginbereich besteht aus zwei Labels für jeweils Einloggen und Registrieren,
    Zwei entry inwelchem der benutzer sein namen eingeben kann 
    und Zwei Buttons für jeweils dem ausführen der Einloggen oder Registrieren Funktion.
    Diese Funktionen liegen in der Controler Datei
    """
    class Login_Window(tk.Frame):
        def __init__(self, master, controler, user):
            super().__init__(master)
            self.master = master
            self.login_Label = tk.Label(self, text = "Einloggen")
            self.login_Label.pack()
            self.login_Entry = tk.Entry(self, text = "Benutzername")
            self.login_Entry.pack()
            self.login_button = tk.Button(self, text= "Login", command = lambda : (controler.login(self.login_Entry, self.master)))
            self.login_button.pack()
            self.signup_label = tk.Label(self, text = "Registrieren")
            self.signup_label.pack()
            self.signup_Entry = tk.Entry(self, text = "Registrieren")
            self.signup_Entry.pack()
            self.signup_button = tk.Button(self, text = "Registrieren", command = lambda : (controler.signup(self.signup_Entry)))
            self.signup_button.pack()
    
    """
    Die Visuelle übersicht für das Generelle Übersichtsfenster mit einer Listbox das alle Filme der Datenbank beinhaltet und
    der anderen Listbox die die vorgeschlagenen Filme beinhaltet. Über der Listbox das alle Filme ausgibt, ist auch eine Suchleiste, mitwelche man bestimmte Filme
    suchen kann. Auf der unteren Seite der Übersicht werden, die Details jedes Filmes angezeigt werden, welche momentan in der Liste ausgewählt ist. 
    """

    class Main_Window(tk.Frame):
        def __init__(self, master, controler, user):
            super().__init__(master)
            self.master = master
            self.user = user
            self.recomended_films = None
            self.controler = controler

            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=0)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            self.Label = tk.Label(self, text="Film-Empfehlungen", font=("Arial", 16, "bold"))
            self.Label.grid(row=0, column=0, columnspan=2, pady=10)

            self.favorites_button = tk.Button(self, text="Favoriten", command=lambda: master.switch_frame(master.Favorites_Window, controler, user))
            self.favorites_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.NE)

            self.film_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.film_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
            self.film_listbox_frame.grid_rowconfigure(3, weight=1)
            self.film_listbox_frame.grid_columnconfigure(0, weight=1)

            tk.Label(self.film_listbox_frame, text="Verfügbare Filme:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)
            tk.Label(self.film_listbox_frame, text="Filmsuche:").grid(row=1, column=0, sticky=tk.W, padx=5)
            self.search_entry = tk.Entry(self.film_listbox_frame)
            self.search_entry.grid(row=1, column=0, sticky=tk.EW, padx=80, pady=5)
            self.search_entry.bind("<KeyRelease>", self.filter_films)

            self.clear_search_button = tk.Button(self.film_listbox_frame, text="Löschen", command=self.clear_search)
            self.clear_search_button.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

            self.film_listbox_scrollbar = tk.Scrollbar(self.film_listbox_frame)
            self.film_listbox_scrollbar.grid(row=3, column=1, sticky=tk.NS)

            self.film_listbox = tk.Listbox(self.film_listbox_frame,
                                        height=15,
                                        yscrollcommand=self.film_listbox_scrollbar.set,
                                        font=("Arial", 12))
            self.film_listbox.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_scrollbar.config(command=self.film_listbox.yview)
            self.film_listbox.bind("<<ListboxSelect>>", self.on_film_select)

            # Right Listbox (Recommended Films)
            self.recommended_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.recommended_listbox_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=10, pady=10)
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=1)
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            tk.Label(self.recommended_listbox_frame, text="Film Empfehlungen:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)

            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                font=("Arial", 12))
            self.recommended_listbox.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)
            self.recommended_listbox.bind("<<ListboxSelect>>", self.on_recommended_select)

            self.details_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
            self.details_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
            self.details_frame.grid_rowconfigure(0, weight=1) # Allow description to expand

            self.film_name_label = tk.Label(self.details_frame, text="Name: Kein Film ausgewählt", font=("Arial", 14, "bold"))
            self.film_name_label.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=(5, 0))

            self.film_description_label = tk.Label(self.details_frame, text="Beschreibung: Wähle zuerst einen Film aus, um die Beschreibung zu sehen.", font=("Arial", 10), wraplength=750, justify=tk.LEFT)
            self.film_description_label.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=(5, 10))

            self.trailer_button = tk.Button(self.details_frame, text="Link Trailer", command=self.perform_film_action, state=tk.DISABLED)
            self.trailer_button.grid(row=2, column=0, sticky=tk.SW, padx=10, pady=(10, 5))

            self.add_film_button = tk.Button(self.details_frame, text = "Favoriten hinzufügen", command = lambda : (self.film_add_to_liked(user)))
            self.add_film_button.grid(row=2, column=1, sticky=tk.SE, padx=10, pady=(10, 5))

            self.list_Films(self.controler.get_Json_Film_Names())
            self.list_recommended_Films(user)
        
        """
        Filme der Userliste unter dem user und favoritefilms hinzufügen.
        """
        def film_add_to_liked(self, user):
            self.controler.write_to_Json(user, self.film_listbox)
            self.list_recommended_Films(user)

        """
        Funktion für das suchen nach den Filmen auf youtube durch das auslesen der Url für den jeweiligen Film
        """
        def perform_film_action(self):
            if self.current_selected_film and "youtubeTrailerUrl" in self.current_selected_film:
                trailer_url = self.current_selected_film["youtubeTrailerUrl"]
                try:
                    webbrowser.open_new_tab(trailer_url)
                except Exception as e:
                    print("Error", f"Could not open trailer link: {e}")
            else:
                print("No Trailer", "No trailer link available for the selected film.")
        
        """
        Für das löschen des Inhaltes der Scuhleiste
        """
        def clear_search(self):
            films = self.controler.get_Json_Film_Names()
            self.search_entry.delete(0, tk.END)
            self.film_listbox(films)
            self.clear_film_details()
        
        """
        für das filtern der Filme die das suchwort beinhalten und die generelle Film Listbox neu ausgibt
        """
        def filter_films(self, event = None):
            search_term = self.search_entry.get().lower()
            films = self.controler.get_Json_Film_Names()
            filtered_films = []
            for film in films:
                if search_term in film.lower():
                    filtered_films.append(film)

            self.list_Films(filtered_films)
        
        """
        Die Funktion wird nach dem selektieren eines Filmes in der Recommended Listbox die Detail übersicht auf der Unteren Seite aktualisieren
        """
        def on_recommended_select(self, event = None):
            try:
                selected_indices = self.recommended_listbox.curselection()
                selected_film_data = {}

                index = selected_indices[0]
                selected_film_name = self.recommended_listbox.get(index)
                selected_film_name = self.film_listbox.get(index)
                selected_film_data = next((film for film in self.controler.get_Json() if film["film_names"] == selected_film_name), None)


                if selected_film_data:
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.current_selected_film = selected_film_data # Store for button action
                else:
                    self.clear_film_details(True)
            except Exception as e:
                print("Error")
        
        """
        Die Funktion wird nach dem selektieren eines Filmes in der generellen Film Listbox die Detail übersicht auf der Unteren Seite aktualisieren
        """

        def on_film_select(self, event = None):
            try:
                selected_indices = self.film_listbox.curselection()
                if not selected_indices:
                    self.clear_film_details(False)
                    return
                
                index = selected_indices[0]
                selected_film_name = self.film_listbox.get(index)
                selected_film_data = next((film for film in self.controler.get_Json()  if film["film_names"] == selected_film_name), None)


                if selected_film_data:
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.add_film_button.config(state=tk.NORMAL)
                    self.current_selected_film = selected_film_data # Store for button action
                else:
                    self.clear_film_details(False)
            except Exception as e:
                print(e)
        
        """
        Die Funktion löscht den Inhalt der Detail übersicht auf der Unteren Seite der Übersicht
        """
        def clear_film_details(self, boolean_recommended):
            self.film_name_label.config(text="Name: ")
            self.film_description_label.config(text="Beschreibung: ")
            
            self.trailer_button.config(state=tk.DISABLED)
            self.add_film_button.config(state=tk.DISABLED)
                
            self.current_selected_film = None

        """
        Die Funktion listet die gegeben Filme in der generellen Listbox auf
        """
        def list_Films(self, films):
            self.film_listbox.delete(0, tk.END) # Clear existing items
            for film in films:
                self.film_listbox.insert(tk.END, film)
        
        """
        Die Funktion listet die gegeben Filme in der recommendet Listbox auf
        """
        def list_recommended_Films(self, user):
            self.recommended_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_recommended_Film_Names(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)

    """
    Die Klasse zeigt das Fenster für die hinzugefügten Filme zu
    """
    class Favorites_Window(tk.Frame):
        def __init__(self, master,controler, user):
            super().__init__(master)
            self.controler = controler
            self.user = user # Ensure user is stored for later use

            # Configure row and column weights for better resizing behavior
            self.grid_rowconfigure(0, weight=0) # For labels and buttons
            self.grid_rowconfigure(1, weight=1) # For the listbox frames
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            # Main title for the window
            self.Label = tk.Label(self, text="Meine Favoriten", font=("Arial", 16, "bold"))
            self.Label.grid(row=0, column=0, columnspan=2, pady=10) # Centered across both columns

            # Button to return to Main Window
            self.Button = tk.Button(self, text="Zurück zum Hauptfenster",
                                    command=lambda: master.switch_frame(master.Main_Window, controler, user))
            self.Button.grid(row=0, column=3, sticky=tk.NW, padx=10, pady=10) # Placed top-left

            # --- First Listbox (Recommended Films) ---
            self.liked_films_listbox_label = tk.Label(self, text="Empfohlene Filme:", font=("Arial", 12, "underline"))
            self.liked_films_listbox_label.grid(row=1, column=0, sticky=tk.SW, padx=5, pady=2)

            self.liked_films_listbox_frame = tk.Frame(self, bd=2, relief="groove") # Added border for visual separation
            self.liked_films_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.liked_films_listbox_frame.grid_rowconfigure(0, weight=1)
            self.liked_films_listbox_frame.grid_columnconfigure(0, weight=1)

            self.liked_films_listbox_scrollbar = tk.Scrollbar(self.liked_films_listbox_frame)
            self.liked_films_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.liked_films_listbox = tk.Listbox(self.liked_films_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.liked_films_listbox_scrollbar.set,
                                                font=("Arial", 11),
                                                selectmode=tk.SINGLE) # Allow single selection
            self.liked_films_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.liked_films_listbox_scrollbar.config(command=self.liked_films_listbox.yview)

            self.remove_liked_button = tk.Button(self.liked_films_listbox_frame, text="Aus Liste entfernen",
                                                command=lambda: self.remove_films(self.user))
            self.remove_liked_button.grid(row=1, column=0, columnspan=2, pady=5) # Below the listbox

            # --- Second Listbox (e.g., Liked Films / Watchlist) ---
            self.watchlist_listbox_label = tk.Label(self, text="Meine Merkliste:", font=("Arial", 12, "underline"))
            self.watchlist_listbox_label.grid(row=1, column=1, sticky=tk.SW, padx=5, pady=2) # Right column

            self.watchlist_listbox_frame = tk.Frame(self, bd=2, relief="groove") # Added border
            self.watchlist_listbox_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5) # Right column
            self.watchlist_listbox_frame.grid_rowconfigure(0, weight=1)
            self.watchlist_listbox_frame.grid_columnconfigure(0, weight=1)

            self.watchlist_listbox_scrollbar = tk.Scrollbar(self.watchlist_listbox_frame)
            self.watchlist_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.watchlist_listbox = tk.Listbox(self.watchlist_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.watchlist_listbox_scrollbar.set,
                                                font=("Arial", 11),
                                                selectmode=tk.SINGLE)
            self.watchlist_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.watchlist_listbox_scrollbar.config(command=self.watchlist_listbox.yview)

            self.add_to_watchlist_button = tk.Button(self.watchlist_listbox_frame, text="Zur Merkliste hinzufügen",
                                                    command=lambda: self.add_to_watchlist(self.user))
            self.add_to_watchlist_button.grid(row=1, column=0, columnspan=2, pady=5)

            # Initial population of the listboxes (dummy data for demonstration)
            self.List_Films(self.user)
            self.List_recommenden_colbrotative_Films(self.user)


        """
        Die Funktion löscht den ausgewählten Film von der watched Listbox
        """
        def List_Films(self, user):
            self.controler.remove_from_list(user, self.liked_films_listbox)
            self.List_Produkts(user)
        
        def List_recommenden_colbrotative_Films(self, user):
            self.watchlist_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_recommended_Films_collarbotive(user)
            for film in Film_names:
                self.watchlist_listbox.insert(tk.END, film)
        
        """
        Die Funktion listet alle Filme des users auf, welche dieser als angesehenen Film klassigiziert
        """
        def List_Films(self, user):
            self.liked_films_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_user_Liked_Films(user)
            for film in Film_names:
                self.liked_films_listbox.insert(tk.END, film)