import tkinter as tk
import View
import Model

class Controler():
    """
    Bei der Initialisierung sollen die relevanten Pfade aufeglistet und für spätere benutzung gespeichert werden.
    Zudem sollen instanzen der view und model klasse, für das rendern und bearbeiten der Daten, erstellt werden.
    """
    def __init__(self):
        user_db_path = r"Python_Projekt\Ohne_Firebase\users.json"
        films_db_path = r"Python_Projekt\Ohne_Firebase\Films.json"

        self.model = Model.Model(user_db_path, films_db_path)
        self.view = View.View(self)

        self.view.mainloop()
    

    """
    Die Login Funktion überprüft, ob der Eingegebene User auch in der Liste exestiert
    """
    def login(self, login_Entry, master):
        users = self.get_Json_User_Names()
        for user_ls in users:
            user = login_Entry.get()
            user = user.strip()
            print(user)
            print(str(user_ls))

            if user == str(user_ls).strip():
                master.switch_frame(master.Main_Window, self, user)
                break
            
            else:
                print("Es gibt den User nicht")
    
    """
    Die Signup Funktion erstellt ein User mit den eingegeben Namen des eingabe Entries
    """
    def signup(self, signup_Entry):
            #Es können mehrere gleiche benutzer exestieren, muss gefixt werden!!!
            user = signup_Entry.get()
            for user_ls in self.get_Json_User_Names():
                if user_ls == user:
                    raise ValueError("Error")
            
            user = user.strip().lower()
            self.model.write_to_signup_json(user)

    #Die get_Json Funktion holt die ganzen Daten einer Json Datei
    def get_Json(self):
        Film_names = self.model.loaded_film_data
        return Film_names
    
    #Die Funktion entnimmt sich alle Film Namen
    def get_Json_Film_Names(self):
        Film_names = self.model.get_films_from_json()
        return Film_names
    
    #Doe Funktion entimmt alle User Namen der User Json
    def get_Json_User_Names(self):
        Film_names = self.model.get_names_from_json()
        return Film_names
    
    #Die Funktion entnimmt alle vorgeschlagenen Filme aus dem Algorythmus
    def get_Json_recommended_Film_Names(self, user):
        Film_names = self.model.get_recommendations(user)
        return Film_names
    
    #Die Funktion entimmt alle gelikte Filmen aus der User json Datei
    def get_Json_user_Liked_Films(self, user):
        Film_names = self.model.get_liked_films_from_jason(user)
        return Film_names
    
    #Die Funktion scheibt die ausgewählten Titel auf die Ausgewählte Datei der Listbox
    def write_to_Json(self,user,Listbox):
        index = Listbox.curselection()
        liked_film = Listbox.get(index)
        self.model.write_to_json(user, liked_film)
    
    #Die Funktion entfernt die ausgewähöte datei einer Listbox
    def remove_from_list(self, user, Listbox):
        try:
            index = Listbox.curselection()
            filename = Listbox.get(index)
            self.model.removed_liked_films_from_jason(user, filename)
        
        except Exception as e:
            print(e)