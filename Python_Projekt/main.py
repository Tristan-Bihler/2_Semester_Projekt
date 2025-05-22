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
    
    k = 0

    for i in range(len(Produkt_liste[Produkt][1])):
            Wertigkeit[i] = int(Wertigkeit[i]) + int(Produkt_liste[Produkt][1][i])
            if Wertigkeit[i] >= k:
                 k = Wertigkeit[i]
                 result = i
    
    T = "Das könnte dir auch Gefallen:\n"
    for P in Produkt_liste:
        if int(Produkt_liste[P][1][result]) >= 1:
            T = T + "\n" + P
            print(T)
    
    label.config(text = T)
    
    print(k)
    print(Wertigkeit)
    print(momentarer_Warenkorb)



if __name__ == "__main__":
    Produkte = fh.load(r"Python_Projekt\Produkt_list.txt")
    Auswahl = []
    
    for i in Produkte:
        Auswahl.append((str(i), Produkte[i][0]))
    
    window = tk.Tk()
    window.geometry("400x200")
    combo = ttk.Combobox(window, values = Auswahl)
    combo.pack()
    button = ttk.Button(window, text="Display selection", command = lambda: Warenkorb(Produkte ,1)).pack()
    label = ttk.Label(window, text = "")
    label.pack()
    window.mainloop()