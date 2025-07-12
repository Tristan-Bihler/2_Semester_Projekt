import tkinter as tk
import webbrowser
from tkinter import messagebox
#-----------------------------------------------------View
class View(tk.Tk):
    def __init__(self,controller):
        super().__init__()
        #Window erstellen mit der 800 pixel breite und 600 pixel höhe, sowie dem namen Film Vorschlags Applikation 
        self.geometry("1000x800")
        self.title("Film Empfehlungs Applikation")
        self.controller = controller
        #Wechseln in das Login Fenster
        self._frame = None
        self.switch_frame(self.Login_Window, controller, None)
        
    #Die Wechselfunktion für das Wechseln verschiedener ansichts Bereiche
    def switch_frame(self, frame_class, controller, user):
        new_frame = frame_class(self, controller, user)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
    """
    Die Visuelle Übersicht für das Login fenster mit verschiedenen Elementen.
    Der Loginbereich besteht aus zwei Labels für jeweils Einloggen und Registrieren,
    Zwei entry inwelchem der benutzer sein namen eingeben kann 
    und Zwei Buttons für jeweils dem ausführen der Einloggen oder Registrieren Funktion.
    Diese Funktionen liegen in der controller Datei
    """
    class Login_Window(tk.Frame):
        def __init__(self, master, controller, user):
            super().__init__(master)
            self.controller = controller
            self.master = master
            self.login_Label = tk.Label(self, text = "Einloggen")
            self.login_Label.pack()
            self.login_Entry = tk.Entry(self, text = "Benutzername")
            self.login_Entry.pack()
            self.login_button = tk.Button(self, text= "Login", command = self.login)
            self.login_button.pack()
            self.signup_label = tk.Label(self, text = "Registrieren")
            self.signup_label.pack()
            self.signup_Entry = tk.Entry(self, text = "Registrieren")
            self.signup_Entry.pack()
            self.signup_button = tk.Button(self, text = "Registrieren", command = self.signup)
            self.signup_button.pack()
        
        #Funktion für das die Anzeige veränderung bei der Registrierung
        def login(self):
            try: 
                self.controller.login(self.login_Entry, self.master)
            
            except Exception as e:
                messagebox.showinfo(message = str(e))
                self.signup_Entry.delete(0, tk.END)
                self.login_Entry.delete(0, tk.END)

        #Funktion für das die Anzeige verädnerung bei der Registrierung 
        def signup(self):
            try: 
                self.controller.signup(self.signup_Entry)
            
            except Exception as e:
                messagebox.showinfo(message = str(e))
                self.signup_Entry.delete(0, tk.END)
                self.login_Entry.delete(0, tk.END)
    """
    Die Visuelle übersicht für das Generelle Übersichtsfenster mit einer Listbox das alle Filme der Datenbank beinhaltet und
    der anderen Listbox die die vorgeschlagenen Filme beinhaltet. Über der Listbox das alle Filme ausgibt, ist auch eine Suchleiste, mitwelche man bestimmte Filme
    suchen kann. Auf der unteren Seite der Übersicht werden, die Details jedes Filmes angezeigt werden, welche momentan in der Liste ausgewählt ist. 
    """

    class Main_Window(tk.Frame):
        def __init__(self, master, controller, user):
            super().__init__(master)
            self.master = master
            self.user = user
            self.recomended_films_data = None
            self.controller = controller

            #Das Fenster eine Struktur geben, somit es besser die elemente anzeigen kann
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=0)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            #Ein Text als Überschrifft für das Fenster erstellen
            self.Label = tk.Label(self, text="Film-Empfehlungen", font=("Arial", 16, "bold"))
            self.Label.grid(row=0, column=0, columnspan=2, pady=10)

            #Ein Button erstellen um auf die Favoriten Übersicht zu kommen
            self.favorites_button = tk.Button(self, text="Favoriten", command=lambda: master.switch_frame(master.Favorites_Window, controller, user))
            self.favorites_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.NE)

            #Die Linke Listenbox erstellen um Alle Filme anzeigen zu können. Allerding hier noch ein übergordneter Frame erstellen, indem die Listenbox, Searchbar und Scrollbar unterlegen sind.
            self.film_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.film_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
            #Den Frame auch wieder eine Struktur geben, in welchen die Elemente dann auch besser dargestellt werden
            self.film_listbox_frame.grid_rowconfigure(0, weight=0)
            self.film_listbox_frame.grid_rowconfigure(1, weight=0)
            self.film_listbox_frame.grid_rowconfigure(2, weight=1)
            self.film_listbox_frame.grid_columnconfigure(0, weight=1)

            #Weitere Titel erstellen für Die Listenbox die alle Filme anzeigt
            tk.Label(self.film_listbox_frame, text="Verfügbare Filme:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)
            tk.Label(self.film_listbox_frame, text="Filmsuche:").grid(row=1, column=0, sticky=tk.W, padx=5)
            #Die Seatchbar, indem Filmnamen eingegeben werden können um diese zu suchen
            self.search_entry = tk.Entry(self.film_listbox_frame)
            self.search_entry.grid(row=1, column=0, sticky=tk.EW, padx=80, pady=5)
            self.search_entry.bind("<KeyRelease>", self.filter_films)

            #Button erstellen um die Suche zurückzusetzen
            self.clear_search_button = tk.Button(self.film_listbox_frame, text="Löschen", command=self.clear_search)
            self.clear_search_button.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
            #Scrollbar erstellen um die Listenbox zu durchsuchen
            self.film_listbox_scrollbar = tk.Scrollbar(self.film_listbox_frame)
            self.film_listbox_scrollbar.grid(row=2, column=1, sticky=tk.NS)

            #Die eigentliche Listenbox um alle Filme anzuzeigen
            self.film_listbox = tk.Listbox(self.film_listbox_frame,
                                        height=15,
                                        yscrollcommand=self.film_listbox_scrollbar.set,
                                        font=("Arial", 12))
            self.film_listbox.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_scrollbar.config(command=self.film_listbox.yview)
            self.film_listbox.bind("<<ListboxSelect>>", self.on_film_select)

            #Die Rechte Listenbox erstellen um Alle Filme anzeigen zu können. Allerding hier noch ein übergordneter Frame erstellen, indem die Listenbox und Scrollbar unterlegen sind.
            self.recommended_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.recommended_listbox_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=10, pady=10)
            #Dem überordneten Frame auch eine Struktur geben
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=0)
            self.recommended_listbox_frame.grid_rowconfigure(1, weight=1)
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            #Weitere Überschriften erstellen
            self.recomended_films_label = tk.Label(self.recommended_listbox_frame, text="Empfohlene Filme:", font=("Arial", 10, "bold"))
            self.recomended_films_label.grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)

            #Scrollbar erstellen
            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=1, column=1, sticky=tk.NS)

            #Die eigentliche Listenbox für die Vorgeschlagenen Liste anzeigen zu können
            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                font=("Arial", 12))
            self.recommended_listbox.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)
            self.recommended_listbox.bind("<<ListboxSelect>>", self.on_recommended_select)

            #Film Detail Übersicht
            #Übergordneter Frame erstellen indem der Titel, die Beschreibung, sowie Trailer Button und dem Hinzufügen zu der Liste untergordnet sind
            self.details_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
            self.details_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
            #Dem Frame eine Struktur geben
            self.details_frame.grid_rowconfigure(0, weight=0)
            self.details_frame.grid_rowconfigure(1, weight=1)
            self.details_frame.grid_rowconfigure(2, weight=0)
            self.details_frame.grid_columnconfigure(0, weight=1)
            self.details_frame.grid_columnconfigure(1, weight=0)

            #Titel für den Film
            self.film_name_label = tk.Label(self.details_frame, text="Name: Kein Film ausgewählt", font=("Arial", 14, "bold"))
            self.film_name_label.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=(5, 0))

            #Beschreibung für den Film
            self.film_description_label = tk.Label(self.details_frame, text="Beschreibung: Wähle zuerst einen Film aus, um die Beschreibung zu sehen.", font=("Arial", 10), wraplength=750, justify=tk.LEFT)
            self.film_description_label.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=(5, 10))

            #Trailer button um den Film auf youtube öffnen zu können
            self.trailer_button = tk.Button(self.details_frame, text="Link Trailer", state=tk.DISABLED, command = self.perform_film_action)
            self.trailer_button.grid(row=2, column=0, sticky=tk.SW, padx=10, pady=(10, 5))

            #Den Button erstellen um den Film zu der Favoriten Liste hinzuzufügen
            self.add_film_button = tk.Button(self.details_frame, text = "Zu Favoriten hinzufügen", state=tk.DISABLED, command = lambda : (self.film_add_to_liked(user)))
            self.add_film_button.grid(row=2, column=1, sticky=tk.SE, padx=10, pady=(10, 5))

            #Listen anzeigen lassen
            self.list_Films(self.controller.get_Json_Film_Names())
            self.list_recommended_Films(user)
        
        """
        Filme der Userliste unter dem user und favoritefilms hinzufügen.
        """
        def film_add_to_liked(self, user):
            try:
                liked_film = self.controller.write_to_Json(user, self.what_listbox)
                self.list_recommended_Films(user)
                raise Exception(f"Der Film, {liked_film}, wurde der Favoritenliste hinzugefügt")

            except Exception as e:
                messagebox.showinfo(message = str(e))
                print(Exception)

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
            films = self.controller.get_Json_Film_Names()
            self.search_entry.delete(0, tk.END)
            self.list_Films(films)
            self.clear_film_details()
        
        """
        für das filtern der Filme die das suchwort beinhalten und die generelle Film Listbox neu ausgibt
        """
        def filter_films(self, event = None):
            search_term = self.search_entry.get().lower()
            films = self.controller.get_Json_Film_Names()
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
                self.what_listbox = self.recommended_listbox
                index = selected_indices[0]
                #Filmliste auf eine Variable speichern
                selected_film_name = self.recommended_listbox.get(index)
                #Jeden Film der Filmliste durchgehen
                for film in self.controller.get_Json():
                    #Abfragen ob der momentane Film der angeklickte film in der Listenbox ist
                    if film["film_names"] == selected_film_name:
                        selected_film_data = film

                if selected_film_data:
                    #Falls der Film exestiert können nun alle Attribute in der Detailübersicht geändert werden
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.add_film_button.config(state=tk.NORMAL)
                    self.current_selected_film = selected_film_data

            except Exception as e:
                print(e)
        
        """
        Die Funktion wird nach dem selektieren eines Filmes in der generellen Film Listbox die Detail übersicht auf der Unteren Seite aktualisieren
        """

        def on_film_select(self, event = None):
            try:
                selected_indices = self.film_listbox.curselection()
                selected_film_data = {}

                index = selected_indices[0]
                self.what_listbox = self.film_listbox
                selected_film_name = self.film_listbox.get(index)
                #Jeden Film der Filmliste durchgehen
                for film in self.controller.get_Json():
                    #Abfragen ob der momentane Film der angeklickte film in der Listenbox ist
                    if film["film_names"] == selected_film_name:
                        selected_film_data = film

                if selected_film_data:
                    #Falls der Film exestiert können nun alle Attribute in der Detailübersicht geändert werden
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.add_film_button.config(state=tk.NORMAL)
                    self.current_selected_film = selected_film_data

            except Exception as e:
                print(e)
        
        """
        Die Funktion löscht den Inhalt der Detail übersicht auf der Unteren Seite der Übersicht
        """
        def clear_film_details(self):
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
            Film_names = self.controller.get_Json_recommended_Film_Names(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)

    """
    Die Klasse zeigt das Fenster für die hinzugefügten Filme zu
    """
    class Favorites_Window(tk.Frame):
        def __init__(self, master,controller, user):
            super().__init__(master)
            #Variablen Initialisieren
            self.master = master
            self.controller = controller
            self.user = user

            # Konfiguriere Zeilen- und Spaltengewichte für besseres Größenverhalten
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=0)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            # Haupttitel für das Fenster
            self.Label = tk.Label(self, text="Meine Favoriten", font=("Arial", 16, "bold"))
            self.Label.grid(row=0, column=0, columnspan=2, pady=10)  # Zentriert über beide Spalten

            # Button zur Rückkehr zum Hauptfenster
            self.Button = tk.Button(self, text="Zurück zum Hauptfenster",
                                    command=lambda: master.switch_frame(master.Main_Window, controller, user))
            self.Button.grid(row=0, column=1, sticky=tk.NE, padx=10, pady=10) # Platziert oben rechts

            # Linke Listbox erstellen, jedoch mit einem übergeordneten Frame und untergeordneten Label und Button
            self.liked_films_listbox_label = tk.Label(self, text="Meine Favoriten:", font=("Arial", 12, "underline"))
            self.liked_films_listbox_label.grid(row=1, column=0, sticky=tk.SW, padx=5, pady=2)

            self.liked_films_listbox_frame = tk.Frame(self, bd=2, relief="groove")  # Rahmen für visuelle Trennung
            self.liked_films_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.liked_films_listbox_frame.grid_rowconfigure(0, weight=1)
            self.liked_films_listbox_frame.grid_rowconfigure(1, weight=0) # Für den Entfernen-Button
            self.liked_films_listbox_frame.grid_columnconfigure(0, weight=1)

            self.liked_films_listbox_scrollbar = tk.Scrollbar(self.liked_films_listbox_frame)
            self.liked_films_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.liked_films_listbox = tk.Listbox(self.liked_films_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.liked_films_listbox_scrollbar.set,
                                                font=("Arial", 11),
                                                selectmode=tk.SINGLE)  # Nur Einzelauswahl zulassen
            self.liked_films_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.liked_films_listbox_scrollbar.config(command=self.liked_films_listbox.yview)
            self.liked_films_listbox.bind("<<ListboxSelect>>", self.on_liked_film_select)

            self.remove_liked_button = tk.Button(self.liked_films_listbox_frame, text="Aus Favoriten entfernen",
                                                command=self.remove_Film_from_liked_listbox)
            self.remove_liked_button.grid(row=1, column=0, columnspan=2, pady=5)

            # Rechte Listbox erstellen, jedoch mit einem übergeordneten Frame und untergeordneten Label und Button
            self.colabrativ_listbox_label = tk.Label(self, text="Nutzern mit ähnlichen Interessen gefiel auch:", font=("Arial", 12, "underline"))
            self.colabrativ_listbox_label.grid(row=1, column=1, sticky=tk.SW, padx=5, pady=2)

            self.colabrativ_listbox_frame = tk.Frame(self, bd=2, relief="groove")
            self.colabrativ_listbox_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5) 
            self.colabrativ_listbox_frame.grid_rowconfigure(0, weight=1)
            self.colabrativ_listbox_frame.grid_rowconfigure(1, weight=0)
            self.colabrativ_listbox_frame.grid_columnconfigure(0, weight=1)

            self.colabrativ_listbox_scrollbar = tk.Scrollbar(self.colabrativ_listbox_frame)
            self.colabrativ_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.colabrativ_listbox = tk.Listbox(self.colabrativ_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.colabrativ_listbox_scrollbar.set,
                                                font=("Arial", 11),
                                                selectmode=tk.SINGLE) # Nur Einzelauswahl zulassen
            self.colabrativ_listbox.grid(row=0, column=0, sticky=tk.NSEW)
            self.colabrativ_listbox_scrollbar.config(command=self.colabrativ_listbox.yview)
            #Die Funktion on_colabrativ_select an die Listbox anbinden, somit bei anklicken einer Reihe diese Funktion getätigt wird
            self.colabrativ_listbox.bind("<<ListboxSelect>>", self.on_colabrativ_select)


            #Detailansichts Frame
            self.details_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
            self.details_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
            #Detailansich struktur
            self.details_frame.grid_rowconfigure(0, weight=0)
            self.details_frame.grid_rowconfigure(1, weight=1)
            self.details_frame.grid_rowconfigure(2, weight=0)
            self.details_frame.grid_columnconfigure(0, weight=1)
            self.details_frame.grid_columnconfigure(1, weight=0) 

            #Filmtitel angeben
            self.film_name_label = tk.Label(self.details_frame, text="Name: Kein Film ausgewählt", font=("Arial", 14, "bold"))
            self.film_name_label.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=(5, 0))

            #Filmbescheibung angeben
            self.film_description_label = tk.Label(self.details_frame, text="Beschreibung: Wähle zuerst einen Film aus, um die Beschreibung zu sehen.", font=("Arial", 10), wraplength=750, justify=tk.LEFT)
            self.film_description_label.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=(5, 10))

            #Trailer button angeben
            self.trailer_button = tk.Button(self.details_frame, text="Link Trailer", state=tk.DISABLED, command=self.perform_film_action)
            self.trailer_button.grid(row=2, column=0, sticky=tk.SW, padx=10, pady=(10, 5))

            #Zur Favoriten Liste button angeben
            self.add_film_button = tk.Button(self.details_frame, text="Zu Favoriten hinzufügen", state=tk.DISABLED, command=lambda: (self.film_add_to_liked(self.user)))
            self.add_film_button.grid(row=2, column=1, sticky=tk.SE, padx=10, pady=(10, 5))

            self.List_Films(self.user)
            self.List_recommenden_colbrotative_Films(self.user)


        """
        Die Funktion fügt den ausgewählten Film der Favoriten Listbox hinzu und aktualisiert darauf die Listen
        """
        def film_add_to_liked(self, user):
            try:
                self.controller.write_to_Json(user, self.colabrativ_listbox)
                self.List_Films(user)
                self.List_recommenden_colbrotative_Films(user)

            except Exception as e:
                messagebox.showinfo(message = str(e))#Genutz für die Mitteilung das der Film der liste hinzugefügt wurde, bzw auch ob ein Problem vorliegt
                #print(Exception)
        
        """
        #Die Funktion für das auflisten der Filme in der Listbox und gegeben Falls auch das aktualisieren
        """
        def List_recommenden_colbrotative_Films(self, user):
            self.colabrativ_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controller.get_Json_recommended_Films_collaborative(user)
            for film in Film_names:
                self.colabrativ_listbox.insert(tk.END, film)
        
        """
        Die Funktion löscht den ausgewählten Film von der Favoriten Listbox und aktualisiert darauf die Listen
        """
        def remove_Film_from_liked_listbox(self):
            try:
                self.controller.remove_from_list(self.user, self.liked_films_listbox)
                self.List_Films(self.user)
                self.List_recommenden_colbrotative_Films(self.user)
            except:
                print(Exception)


        """
        Die Funktion listet alle Filme des users auf, welche dieser als Favoriten Film klassifiziert
        """
        def List_Films(self, user):
            self.liked_films_listbox.delete(0, tk.END)
            Film_names = self.controller.get_Json_user_Liked_Films(user)
            for film in Film_names:
                self.liked_films_listbox.insert(tk.END, film)
        
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
        Die Funktion wird nach dem selektieren eines Filmes in der Recommended Listbox die Detail übersicht auf der Unteren Seite aktualisieren
        """
        def on_colabrativ_select(self, event = None):
            try:
                selected_indices = self.colabrativ_listbox.curselection()
                selected_film_data = {}
                #print(selected_indices)
                index = selected_indices[0]
                selected_film_name = self.colabrativ_listbox.get(index)
                #Jeden Film der Filmliste durchgehen
                for film in self.controller.get_Json():
                    #Abfragen ob der momentane Film der angeklickte film in der Listenbox ist
                    if film["film_names"] == selected_film_name:
                        selected_film_data = film

                #Falls der Film exestiert können nun alle Attribute in der Detailübersicht geändert werden
                if selected_film_data:
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.add_film_button.config(state=tk.NORMAL)
                    self.current_selected_film = selected_film_data

            except Exception as e:
                print(e)
        
        """
        Die Funktion wird nach dem selektieren eines Filmes in der generellen Film Listbox die Detail übersicht auf der Unteren Seite aktualisieren
        """
        def on_liked_film_select(self, event = None):
            try:
                selected_indices = self.liked_films_listbox.curselection()
                selected_film_data = {}
                #print(selected_indices)
                index = selected_indices[0]
                selected_film_name = self.liked_films_listbox.get(index)
                #Jeden Film der Filmliste durchgehen
                for film in self.controller.get_Json():
                    #Abfragen ob der momentane Film der angeklickte film in der Listenbox ist
                    if film["film_names"] == selected_film_name:
                        selected_film_data = film
                
                #Falls der Film exestiert können nun alle Attribute in der Detailübersicht geändert werden
                if selected_film_data:
                    self.film_name_label.config(text=f"Name: {selected_film_data['film_names']}")
                    self.film_description_label.config(text=f"Beschreibung: {selected_film_data['beschreibung']}")
                    self.trailer_button.config(state=tk.NORMAL)
                    self.add_film_button.config(state=tk.DISABLED)
                    self.current_selected_film = selected_film_data

            except Exception as e:
                print("on_liked_film_select: ")
                print(e)