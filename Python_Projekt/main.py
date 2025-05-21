"""
Projekt:        Empfehlungsystem     
Ersteller:      Halter Carina, Mirwald Laura, Finé Semian, Bihler Tristan
Version:        0.0.1    

Über das Projekt:
    
"""
import tkinter as tk
from tkinter import ttk
import File_handling as fh

momentarer_Warenkorb = {}
Wertigkeit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def Warenkorb(Produkt_liste, menge):
    Produkt = combo.get()
    Produkt = Produkt.split(" ")
    Produkt = Produkt[0]
    try:
        momentarer_Warenkorb[Produkt] = (Produkt_liste[Produkt][0], momentarer_Warenkorb[Produkt][1] + menge)
        
    except:
        momentarer_Warenkorb[Produkt] = (Produkt_liste[Produkt][0], menge)
    
    for i in range(len(Produkt_liste[Produkt][1])):
            Wertigkeit[i] = int(Wertigkeit[i]) + int(Produkt_liste[Produkt][1][i])
    
    print(Wertigkeit)
    print(momentarer_Warenkorb)



if __name__ == "__main__":
    Produkte = fh.load(r"Python_Projekt\Produkt_list.txt")
    Auswahl = []
    
    for i in Produkte:
        Auswahl.append((i, Produkte[i][0]))
    
    window = tk.Tk()
    combo = ttk.Combobox(window, values = Auswahl)
    combo.pack()
    button = ttk.Button(text="Display selection", command = lambda: Warenkorb(Produkte ,1)).pack()
    window.mainloop()