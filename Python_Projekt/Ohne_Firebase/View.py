import tkinter as tk
import File_handling as Fh
import Python_Projekt.Ohne_Firebase.Model as Model

class ui(tk.Tk):
    def __init__(self):
        super().__init__()
        #Window erstellen mit der 800 pixel breite und 600 pixel höhe, sowie dem namen Film Vorschlags Applikation 
        self.geometry("800x600")
        self.title("Film Vorschlags Applikation")
        
        self._frame = None
        self.switch_frame(Login_Window)

        #Das erstellte Window soll bei jeglicher aktivität neu laden und aktualisieren
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
        self.Label = tk.Label(self, text = "Hello")
        self.Label.pack()
        self.Button = tk.Button(self, text= "Login", command = lambda : master.switch_frame(Main_Window))
        self.Button.pack()

class Main_Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
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

        self.List_Produkts()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    
    def List_Produkts(self):
        Films = Fh.load(r"Python_Projekt\Ohne_Firebase\Films.txt")
        #print(Films)
        #Hier muss der Algorythmus rein
        for Film in Films:
            Film = Film.split(",")
            Film_kachel_instance = Film_Kachel(self.films_frame, Film)
            Film_kachel_instance.pack()
            #print(Film[0])

class Film_Kachel(tk.Frame):
        def __init__(self,master, Film):
            super().__init__(master)
            Film_Name = tk.Label(self, text = Film[0])
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
        Films = Fh.load(r"Python_Projekt\Ohne_Firebase\Films.txt")
        #print(Films)
        for Film in Films:
            Film = Film.split(",")
            Film_kachel_instance = Liked_Film_Kachel(self.films_frame, Film)
            Film_kachel_instance.pack()
            #print(Film[0])
