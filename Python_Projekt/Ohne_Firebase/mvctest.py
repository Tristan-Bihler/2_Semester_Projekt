import tkinter as tk
from tkinter import messagebox

# --- Model (Modell) ---
# Das Model enthält die Daten (den Zählerwert) und die Geschäftslogik.
# Es weiß nichts über die Benutzeroberfläche (View) oder den Controller.
class CounterModel:
    def __init__(self):
        # Initialisiert den Zählerwert
        self._count = 0
        # Eine Liste von "Beobachtern" (in unserem Fall der Controller),
        # die benachrichtigt werden, wenn sich der Zähler ändert.
        self._observers = []

    def get_count(self):
        """Gibt den aktuellen Zählerwert zurück."""
        return self._count

    def increment(self):
        """Erhöht den Zählerwert und benachrichtigt die Beobachter."""
        self._count += 1
        self._notify_observers()

    def decrement(self):
        """Verringert den Zählerwert und benachrichtigt die Beobachter."""
        self._count -= 1
        self._notify_observers()

    def reset(self):
        """Setzt den Zählerwert auf 0 zurück und benachrichtigt die Beobachter."""
        self._count = 0
        self._notify_observers()

    def add_observer(self, observer):
        """Fügt einen Beobachter hinzu, der bei Änderungen benachrichtigt wird."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Entfernt einen Beobachter."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self):
        """Benachrichtigt alle registrierten Beobachter über eine Änderung."""
        for observer in self._observers:
            observer.model_changed()

# --- View (Ansicht) ---
# Die View ist für die Darstellung der Benutzeroberfläche zuständig.
# Sie zeigt die Daten aus dem Model an, enthält aber keine Geschäftslogik
# und weiß nichts über den Controller, außer dass sie Ereignisse an ihn weiterleitet.
class CounterView:
    def __init__(self, master, controller):
        # master ist das übergeordnete Tkinter-Fenster
        self.master = master
        # Der Controller, an den Benutzereingaben weitergeleitet werden
        self.controller = controller
        master.title("MVC Zähler")
        master.geometry("300x200") # Setzt die Fenstergröße
        master.resizable(False, False) # Macht das Fenster nicht in der Größe veränderbar

        # Konfiguriere die Schriftart für ein besseres Aussehen
        default_font = ("Inter", 16)
        button_font = ("Inter", 12, "bold")

        # Zentrales Frame für Inhalt
        main_frame = tk.Frame(master, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Label zur Anzeige des Zählerwerts
        self.count_label = tk.Label(main_frame, text="Zähler: 0", font=default_font, bg="#f0f0f0", fg="#333")
        self.count_label.pack(pady=15)

        # Frame für Schaltflächen
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Schaltfläche zum Erhöhen
        self.increment_button = tk.Button(
            button_frame,
            text="+",
            command=self.controller.handle_increment, # Leitet Klick an Controller weiter
            font=button_font,
            bg="#4CAF50", fg="white", # Grün
            activebackground="#45a049",
            relief="raised",
            padx=10, pady=5,
            bd=0, # Kein Rand
            highlightbackground="#4CAF50" # Für macOS
        )
        self.increment_button.pack(side=tk.LEFT, padx=5)

        # Schaltfläche zum Verringern
        self.decrement_button = tk.Button(
            button_frame,
            text="-",
            command=self.controller.handle_decrement, # Leitet Klick an Controller weiter
            font=button_font,
            bg="#f44336", fg="white", # Rot
            activebackground="#da190b",
            relief="raised",
            padx=10, pady=5,
            bd=0,
            highlightbackground="#f44336"
        )
        self.decrement_button.pack(side=tk.LEFT, padx=5)

        # Schaltfläche zum Zurücksetzen
        self.reset_button = tk.Button(
            button_frame,
            text="Zurücksetzen",
            command=self.controller.handle_reset, # Leitet Klick an Controller weiter
            font=button_font,
            bg="#2196F3", fg="white", # Blau
            activebackground="#0b7dda",
            relief="raised",
            padx=10, pady=5,
            bd=0,
            highlightbackground="#2196F3"
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Passe das Padding der Buttons an
        for btn in [self.increment_button, self.decrement_button, self.reset_button]:
            btn.config(width=8) # Einheitliche Breite für Buttons

    def update_count_display(self, count):
        """Aktualisiert die Anzeige des Zählers im Label."""
        self.count_label.config(text=f"Zähler: {count}")

# --- Controller (Steuerung) ---
# Der Controller ist der Vermittler. Er empfängt Benutzereingaben von der View,
# aktualisiert das Model und weist die View an, sich zu aktualisieren.
# Er fungiert auch als "Beobachter" des Models.
class CounterController:
    def __init__(self, root):
        # Das Model instanziieren
        self.model = CounterModel()
        # Die View instanziieren und den Controller an die View übergeben
        self.view = CounterView(root, self)

        # Den Controller als Beobachter beim Model registrieren,
        # damit er benachrichtigt wird, wenn sich der Model-Zustand ändert.
        self.model.add_observer(self)

        # Initial die Anzeige aktualisieren
        self.model_changed()

    # Methoden zur Behandlung von Benutzereingaben (von der View aufgerufen)
    def handle_increment(self):
        """Behandelt den Klick auf die Erhöhen-Schaltfläche."""
        self.model.increment()

    def handle_decrement(self):
        """Behandelt den Klick auf die Verringern-Schaltfläche."""
        self.model.decrement()

    def handle_reset(self):
        """Behandelt den Klick auf die Zurücksetzen-Schaltfläche."""
        self.model.reset()

    # Methode, die vom Model aufgerufen wird, wenn sich der Zustand ändert
    def model_changed(self):
        """Wird vom Model aufgerufen, um die View zu aktualisieren."""
        current_count = self.model.get_count()
        self.view.update_count_display(current_count)

# --- Hauptanwendung ---
if __name__ == "__main__":
    # Erstellt das Hauptfenster von Tkinter
    root = tk.Tk()
    # Erstellt eine Instanz des Controllers.
    # Der Controller ist der Startpunkt der Anwendung im MVC-Muster.
    app = CounterController(root)
    # Startet die Tkinter-Ereignisschleife
    root.mainloop()

