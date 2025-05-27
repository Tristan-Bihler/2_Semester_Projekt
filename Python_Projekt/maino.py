import tkinter as tk
from tkinter import ttk
import File_handling as fh

class Einkaufshaus:
    def __init__(self, Produkte):

        self.momentarer_Warenkorb = {}
        self.Wertigkeit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.result = 0

        self.window = tk.Tk()
        self.window.geometry("400x200")

        self.produkt_frame = tk.Frame(self.window)
        self.produkt_frame.grid(row = 0, column = 0)

        self.recomended_frame = tk.Frame(self.window, bg= "black")
        self.recomended_frame.grid(row = 0, column = 1)

        for P in Produkte:
            #Auswahl.append((str(i), Produkte[i][0]))
            self.Produktkacheln(Produkte, P)
        
        for P in Produkte:
            if int(Produkte[P][1][self.result]) >= 1:
                self.Rekommendedkachel(self.recomended_frame, str(P))

        self.window.mainloop()       

    def Einkaufswagen(self, Produkt_liste,Produkt, menge):
        Produkt = Produkt.split(" ")
        Produkt = Produkt[0]
        try:
            self.momentarer_Warenkorb[Produkt] = (Produkt_liste[Produkt][0], self.momentarer_Warenkorb[Produkt][1] + menge)
            
        except:
            self.momentarer_Warenkorb[Produkt] = (Produkt_liste[Produkt][0], menge)
        
        k = 0

        for i in range(len(Produkt_liste[Produkt][1])):
                self.Wertigkeit[i] = int(self.Wertigkeit[i]) + int(Produkt_liste[Produkt][1][i])
                if self.Wertigkeit[i] >= k:
                    k = self.Wertigkeit[i]
                    self.result = i
    
    def Produktkacheln(self, Produkte, name):
        label = ttk.Label(self.produkt_frame, text = name)
        label.pack()
        button = ttk.Button(self.produkt_frame, text = "Kaufen", command =  lambda: self.Einkaufswagen(self, Produkte, name ,1))
        button.pack()

    def Rekommendedkachel(self, Produkte, name):
        label = ttk.Label(self.produkt_frame, text = name)
        label.pack()
        button = ttk.Button(self.produkt_frame, text = "Kaufen", command =  lambda: self.Einkaufswagen(self, Produkte, name ,1))
        button.pack()

    def Suchfunktioner():
        pass

if __name__ == "__main__":
    Produkte = fh.load(r"Python_Projekt\Produkt_list.txt")
    Übersicht = Einkaufshaus(Produkte)
    
