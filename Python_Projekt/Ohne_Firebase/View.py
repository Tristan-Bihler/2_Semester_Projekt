import tkinter as tk
import webbrowser
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
            self.signup_button = tk.Button(self, text = "Signup", command = lambda : (controler.signup(self.signup_Entry)))
            self.signup_button.pack()

    class Main_Window(tk.Frame):
        def __init__(self, master, controler, user):
            super().__init__(master)
            self.master = master
            self.user = user
            self.recomended_films = None
            self.controler = controler

            # Configure grid to expand with window
            # Row 0: Title
            # Row 1: Favorites button (top right)
            # Row 2: Listboxes (side-by-side in the middle)
            # Row 3: Film details (description, name, button)
            self.grid_rowconfigure(0, weight=0) # Title row, fixed size
            self.grid_rowconfigure(1, weight=0) # Favorites button row, fixed size
            self.grid_rowconfigure(2, weight=1) # Listboxes row, takes available space
            self.grid_rowconfigure(3, weight=0) # Details row, fixed size

            self.grid_columnconfigure(0, weight=1) # Left column for left listbox
            self.grid_columnconfigure(1, weight=1) # Right column for right listbox

            # --- 1. Title (Top Centered) ---
            self.Label = tk.Label(self, text="Movie Recommender", font=("Arial", 16, "bold"))
            # Use columnspan=2 to center it across both main columns
            self.Label.grid(row=0, column=0, columnspan=2, pady=10)

            # --- 2. Favorites Button (Top Right) ---
            self.favorites_button = tk.Button(self, text="Favorites", command=lambda: master.switch_frame(master.Favorites_Window, controler, user))
            # Place it in the top right, spanning only the right column effectively
            # sticky=tk.NE pushes it to the North-East (top-right)
            self.favorites_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.NE)

            # --- 3. Listboxes (Middle, Next to Each Other) ---

            # Left Listbox (Available Films)
            self.film_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.film_listbox_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10) # row 2, column 0
            self.film_listbox_frame.grid_rowconfigure(3, weight=1) # Listbox itself
            self.film_listbox_frame.grid_columnconfigure(0, weight=1)

            tk.Label(self.film_listbox_frame, text="Available Films:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)
            tk.Label(self.film_listbox_frame, text="Search Film:").grid(row=1, column=0, sticky=tk.W, padx=5)
            self.search_entry = tk.Entry(self.film_listbox_frame)
            self.search_entry.grid(row=1, column=0, sticky=tk.EW, padx=80, pady=5) # Adjust padx to align
            self.search_entry.bind("<KeyRelease>", self.filter_films)

            self.clear_search_button = tk.Button(self.film_listbox_frame, text="Clear", command=self.clear_search)
            self.clear_search_button.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5) # Align to the right of the search entry

            self.film_listbox_scrollbar = tk.Scrollbar(self.film_listbox_frame)
            self.film_listbox_scrollbar.grid(row=3, column=1, sticky=tk.NS)

            self.film_listbox = tk.Listbox(self.film_listbox_frame,
                                        height=15,
                                        yscrollcommand=self.film_listbox_scrollbar.set,
                                        font=("Arial", 12))
            self.film_listbox.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.film_listbox_scrollbar.config(command=self.film_listbox.yview)
            self.film_listbox.bind("<<ListboxSelect>>", self.on_film_select) # Bind selection event

            # Right Listbox (Recommended Films)
            self.recommended_listbox_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            self.recommended_listbox_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=10, pady=10) # row 2, column 1
            self.recommended_listbox_frame.grid_rowconfigure(0, weight=1) # Listbox itself
            self.recommended_listbox_frame.grid_columnconfigure(0, weight=1)

            tk.Label(self.recommended_listbox_frame, text="Recommended Films:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)

            self.recommended_listbox_scrollbar = tk.Scrollbar(self.recommended_listbox_frame)
            self.recommended_listbox_scrollbar.grid(row=0, column=1, sticky=tk.NS)

            self.recommended_listbox = tk.Listbox(self.recommended_listbox_frame,
                                                height=15,
                                                yscrollcommand=self.recommended_listbox_scrollbar.set,
                                                font=("Arial", 12))
            self.recommended_listbox.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.recommended_listbox_scrollbar.config(command=self.recommended_listbox.yview)

            # --- 4. Film Details (Description, Film Name, Button) - On the Bottom ---
            self.details_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
            # This frame now spans both columns in row 3
            self.details_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
            self.details_frame.grid_rowconfigure(0, weight=1) # Allow description to expand

            self.film_name_label = tk.Label(self.details_frame, text="Name: No Film Selected", font=("Arial", 14, "bold"))
            self.film_name_label.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=(5, 0))

            self.film_description_label = tk.Label(self.details_frame, text="Beschreibung: Select a film from the lists above to see its details.", font=("Arial", 10), wraplength=750, justify=tk.LEFT)
            self.film_description_label.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=(5, 10))

            self.trailer_button = tk.Button(self.details_frame, text="Watch Trailer", command=self.perform_film_action, state=tk.DISABLED)
            self.trailer_button.grid(row=2, column=0, sticky=tk.SW, padx=10, pady=(10, 5))

            self.add_film_button = tk.Button(self.details_frame, text = "add to watch_list", command = lambda : (self.film_add_to_liked(user)))
            self.add_film_button.grid(row = 2, column = 1)
            # Initial population of listboxes (assuming these methods exist)

            self.list_Films(self.controler.get_Json_Film_Names())
            self.list_recommended_Films(user)
        
        def film_add_to_liked(self, user):
            self.controler.write_to_Json(user, self.film_listbox)
            self.list_recommended_Films(user)

        def perform_film_action(self):
            if self.current_selected_film and "youtubeTrailerUrl" in self.current_selected_film:
                trailer_url = self.current_selected_film["youtubeTrailerUrl"]
                try:
                    webbrowser.open_new_tab(trailer_url)
                except Exception as e:
                    print("Error", f"Could not open trailer link: {e}")
            else:
                print("No Trailer", "No trailer link available for the selected film.")


        def clear_search(self):
            films = self.controler.get_Json_Film_Names()
            self.search_entry.delete(0, tk.END)
            self.film_listbox(films)
            self.clear_film_details()
        
        def clear_film_details(self):
            self.film_name_label.config(text="Name: ")
            self.film_description_label.config(text="Beschreibung: ")
            self.trailer_button.config(state=tk.DISABLED)
            self.current_selected_film = None

        def filter_films(self, event = None):
            search_term = self.search_entry.get().lower()
            films = self.controler.get_Json_Film_Names()
            filtered_films = []
            for film in films:
                if search_term in film.lower():
                    filtered_films.append(film)

            print(filtered_films)   
            self.list_Films(filtered_films)
        
        def on_film_select(self, event):
            selected_indices = self.film_listbox.curselection()
            if not selected_indices:
                self.clear_film_details()
                return

            index = selected_indices[0]
            selected_film_name = self.film_listbox.get(index)

            selected_film_data = next((film for film in self.controler.get_Json()  if film["name"] == selected_film_name), None)

            if selected_film_data:
                self.film_name_label.config(text=f"Name: {selected_film_data['name']}")
                self.film_description_label.config(text=f"Description: {selected_film_data['description']}")
                self.trailer_button.config(state=tk.NORMAL)
                self.current_selected_film = selected_film_data # Store for button action
            else:
                self.clear_film_details()

        def list_Films(self, films):
            self.film_listbox.delete(0, tk.END) # Clear existing items
            for film in films:
                self.film_listbox.insert(tk.END, film)
        
        def list_recommended_Films(self, user):
            self.recommended_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_recommended_Film_Names(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)

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

            self.remove_liked_button = tk.Button(self, text = "Remove from List", command = lambda : (self.remove_films(user)))
            self.remove_liked_button.grid()

            self.List_Produkts(user)

        def remove_films(self, user):
            self.controler.remove_from_list(user, self.recommended_listbox)
            self.List_Produkts(user)
        
        def List_Produkts(self, user):
            self.recommended_listbox.delete(0, tk.END) # Clear existing items
            Film_names = self.controler.get_Json_user_Liked_Films(user)
            for film in Film_names:
                self.recommended_listbox.insert(tk.END, film)