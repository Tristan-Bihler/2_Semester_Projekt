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
result = 0

def Warenkorb(recomended_frame, Produkt_liste,Produkt, menge):
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
    
    #label.config(text = T)
    
    print(k)
    print(Wertigkeit)
    print(momentarer_Warenkorb)

def Produktkachel(recomended_frame, Produkte, window, name):
    label = ttk.Label(window, text = name).pack()
    button = ttk.Button(window, text = "Kaufen", command =  lambda: Warenkorb(recomended_frame,Produkte, name ,1))
    button.pack()

def recomendedkachel(recomended_frame, name):
    label = ttk.Label(recomended_frame, text = name)
    label.pack()
    button = ttk.Button(recomended_frame, text = "Kaufen")
    button.pack()

if __name__ == "__main__":
    Produkte = fh.load(r"Python_Projekt\Produkt_list.txt")
    Auswahl = []
    
    window = tk.Tk()
    window.geometry("400x200")

    produkt_frame = tk.Frame(window)
    produkt_frame.grid(row = 0, column = 0)

    recomended_frame = tk.Frame(window, bg= "black")
    recomended_frame.grid(row = 1, column = 1)

    for P in Produkte:
        if int(Produkte[P][1][result]) >= 1:
            recomendedkachel(recomended_frame, str(P))


    for i in Produkte:
        #Auswahl.append((str(i), Produkte[i][0]))
        Produktkachel(recomended_frame, Produkte, produkt_frame, i)


    #combo = ttk.Combobox(window, values = Auswahl)
    #combo.pack()
    #button = ttk.Button(window, text="Display selection", command = lambda: Warenkorb(Produkte ,1)).pack()
    #label = ttk.Label(window, text = "")
    #label.pack()
    window.mainloop()