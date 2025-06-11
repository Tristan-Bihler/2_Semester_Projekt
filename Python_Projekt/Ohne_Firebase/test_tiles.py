import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser # New import for opening web links
import random

class FilmSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Selector")
        self.root.geometry("800x600")

        self.films = self.load_film_data() # Load your film data

        # --- Frames ---
        self.search_frame = ttk.Frame(root, padding="10")
        self.search_frame.pack(fill=tk.X)

        self.list_frame = ttk.Frame(root, padding="10")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.details_frame = ttk.Frame(root, padding="10", relief=tk.GROOVE, borderwidth=2)
        self.details_frame.pack(fill=tk.BOTH, expand=True)

        # --- Search Widgets ---
        self.search_label = ttk.Label(self.search_frame, text="Search Film:")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_films) # Live search

        self.clear_search_button = ttk.Button(self.search_frame, text="Clear", command=self.clear_search)
        self.clear_search_button.pack(side=tk.LEFT, padx=(5, 0))

        # --- Listbox and Scrollbar ---
        self.listbox_label = ttk.Label(self.list_frame, text="Available Films:")
        self.listbox_label.pack(anchor=tk.NW)

        self.listbox_scrollbar = ttk.Scrollbar(self.list_frame)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.film_listbox = tk.Listbox(self.list_frame,
                                       height=15,
                                       yscrollcommand=self.listbox_scrollbar.set,
                                       font=("Arial", 12))
        self.film_listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox_scrollbar.config(command=self.film_listbox.yview)

        self.film_listbox.bind("<<ListboxSelect>>", self.on_film_select)

        # --- Details Widgets ---
        self.selected_film_label = ttk.Label(self.details_frame, text="Selected Film Details:", font=("Arial", 14, "bold"))
        self.selected_film_label.pack(pady=(0, 10), anchor=tk.NW)

        self.film_name_label = ttk.Label(self.details_frame, text="Name: ", font=("Arial", 12, "bold"))
        self.film_name_label.pack(anchor=tk.NW)

        self.film_description_label = ttk.Label(self.details_frame, text="Description: ", font=("Arial", 10), wraplength=750, justify=tk.LEFT)
        self.film_description_label.pack(anchor=tk.NW, pady=(5, 10))

        self.trailer_button = ttk.Button(self.details_frame, text="Watch Trailer", command=self.perform_film_action, state=tk.DISABLED)
        self.trailer_button.pack(pady=(10, 0), anchor=tk.SW)


        self.populate_listbox(self.films) # Initial population

    def load_film_data(self):
        # Sample film data with YouTube trailer links
        sample_films = [
            {"name": "The Grand Budapest Hotel", "description": "The adventures of Gustave H, a legendary concierge at a famous hotel from the interwar period, and Zero Moustafa, the lobby boy who becomes his most trusted friend.", "trailer_link": "https://www.youtube.com/watch?v=1Fg5iXgiF_g"},
            {"name": "Parasite", "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "trailer_link": "https://www.youtube.com/watch?v=5xH0HfjhsaY"},
            {"name": "Spirited Away", "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.", "trailer_link": "https://www.youtube.com/watch?v=fXy-b2jYF-g"},
            {"name": "Arrival", "description": "A linguist is recruited by the military to assist in translating alien communications.", "trailer_link": "https://www.youtube.com/watch?v=tFMo3EF4RQk"},
            {"name": "Blade Runner 2049", "description": "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who's been missing for 30 years.", "trailer_link": "https://www.youtube.com/watch?v=gCcx85zFxMs"},
            {"name": "Interstellar", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "trailer_link": "https://www.youtube.com/watch?v=zSWdZVtXT7E"},
            {"name": "Eternal Sunshine of the Spotless Mind", "description": "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.", "trailer_link": "https://www.youtube.com/watch?v=0kPz_vngd_E"},
            {"name": "Pulp Fiction", "description": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "trailer_link": "https://www.youtube.com/watch?v=s75_P-FmCUs"},
            {"name": "The Matrix", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "trailer_link": "https://www.youtube.com/watch?v=vKQi3bBA1y8"},
            {"name": "Inception", "description": "A thief who steals corporate secrets through use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "trailer_link": "https://www.youtube.com/watch?v=YoHD9XEInc0"},
            {"name": "Whiplash", "description": "A promising young drummer enrolls at a cutthroat music conservatory where his ruthless instructor will stop at nothing to realize a student's potential.", "trailer_link": "https://www.youtube.com/watch?v=7d_jQycdQGY"}
        ]
        return sorted(sample_films, key=lambda x: x["name"]) # Sort by name

    def populate_listbox(self, film_list):
        self.film_listbox.delete(0, tk.END) # Clear existing items
        for film in film_list:
            self.film_listbox.insert(tk.END, film["name"])

    def on_film_select(self, event):
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
            self.clear_film_details()

    def clear_film_details(self):
        self.film_name_label.config(text="Name: ")
        self.film_description_label.config(text="Description: ")
        self.trailer_button.config(state=tk.DISABLED)
        self.current_selected_film = None

    def filter_films(self, event=None):
        search_term = self.search_entry.get().lower()
        filtered_films = [
            film for film in self.films
            if search_term in film["name"].lower() or search_term in film["description"].lower()
        ]
        self.populate_listbox(filtered_films)
        self.clear_film_details() # Clear details when filter changes

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.populate_listbox(self.films)
        self.clear_film_details()

    def perform_film_action(self):
        if self.current_selected_film and "trailer_link" in self.current_selected_film:
            trailer_url = self.current_selected_film["trailer_link"]
            try:
                webbrowser.open_new_tab(trailer_url)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open trailer link: {e}")
        else:
            messagebox.showwarning("No Trailer", "No trailer link available for the selected film.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FilmSelectorApp(root)
    root.mainloop()