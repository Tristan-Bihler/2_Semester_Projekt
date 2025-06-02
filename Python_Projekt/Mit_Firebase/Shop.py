import tkinter as tk
from tkinter import ttk
import Kunde

class Main_Window(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.geometry("400x200")
        Produkte = ""

        self.produkt_frame = Produkt_Window(Produkte)

        self.login_frame = Login_Window(user, self.produkt_frame)
        self.login_frame.pack(fill = "both", expand = True)

class Login_Window(tk.Frame):
    def __init__(self, user, produkt_frame):
        super().__init__()
        self.auth = user.login
        self.config(bg = "Black")

        email_entry = tk.Entry(self)
        email_entry.pack()

        password_entry = tk.Entry(self)
        password_entry.pack()

        login_label = tk.Label(self, text = "Hallo")
        login_label.pack()

        login = tk.Button(self, text = "Login", command = lambda: (self.login_funktion(user, email_entry, password_entry)))
        login.pack()

    def login_funktion(self,user, email_entry, password_entry):
        email = email_entry.get()
        password = password_entry.get()

        user = user.login(email, password)
        
        self.user = user

        print(self.user)

    def logged_in(self, produkt_frame):
        produkt_frame.pack(fill = "both", expand = True)
        self.pack_forget()

class Produkt_Window(tk.Frame):
    def __init__(self, Produkte):
        super().__init__()
        self.config(bg = "Blue")

        for P in Produkte:
            self.Produktkacheln(Produkte, P)
        
        for P in Produkte:
            if int(Produkte[P][1][self.result]) >= 1:
                self.Rekommendedkachel(self, str(P))


    def Produktkacheln(self, Produkte, name):
        label = ttk.Label(self.produkt_frame, text = name)
        label.grid(row=0, column=0)
        button = ttk.Button(self.produkt_frame, text = "Kaufen", command =  lambda: self.Einkaufswagen(self, Produkte, name ,1))
        button.grid(row=1, column=1)

    def Rekommendedkachel(self, Produkte, name):
        label = ttk.Label(self.produkt_frame, text = name)
        label.pack()
        button = ttk.Button(self.produkt_frame, text = "Kaufen", command =  lambda: self.Einkaufswagen(self, Produkte, name ,1))
        button.pack()

    def Suchfunktion():
        pass

class Einkaufswagen():
    def __init__(self):
        pass

    def Warenkorb_Kacheln(self):
        pass
