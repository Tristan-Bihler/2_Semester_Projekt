import tkinter as tk
import View
import Model

class Controller():
    """
    Bei der Initialisierung sollen die relevanten Pfade aufeglistet und für spätere benutzung gespeichert werden.
    Zudem sollen instanzen der view und model klasse, für das rendern und bearbeiten der Daten, erstellt werden.
    """
    def __init__(self):
        #Datenbankpfade bestimmen
        self.user_db_path = r"Python_Projekt\Ohne_Firebase\users.json"
        self.films_db_path = r"Python_Projekt\Ohne_Firebase\Films.json"

        #Model und View Initialisieren
        self.model = Model.Model(self.user_db_path, self.films_db_path)
        self.view = View.View(self)
        
        #Das Tkinter Fenster ausgeben
        self.view.mainloop()
    

    """
    Die Login Funktion überprüft, ob der Eingegebene User auch in der Liste existiert
    """
    def login(self, login_Entry, master):
        try:
            #Jegliche user abgreifen
            users = self.get_Json_User_Names()
            #Jeden user durchgehen
            for user_ls in users:
                user = login_Entry.get()
                user = str(user).strip().lower()
                #Überprüfen, das der User exestiert
                if user == str(user_ls).strip():
                    master.switch_frame(master.Main_Window, self, user)
                    return
                
                else:
                    pass
                    #print("Es gibt den User nicht")

            raise Exception("User existiert nicht")
        
        except Exception as e:
            raise e
    
    """
    Die Signup Funktion erstellt ein User mit den eingegeben Namen des eingabe Entries
    """
    def signup(self, signup_Entry):
            try:
                #Usernamen eingabe
                user = signup_Entry.get()
                user = str(user).lower()
                #Jeden User in der User Datenbank durchgehen
                for user_ls in self.get_Json_User_Names():
                    #Überprüfen ob es den User schon gibt und falls ja das Programm hier unterbrechen und als Problem zurückgeben, das es den Nutzer schon gibt
                    if user_ls == user:
                        raise Exception("Nutzer existiert schon")
                
                user = user.strip().lower()
                #Falls alles gepast hat den Nutzer der Liste hinzufügen und als Meldung zurückgeben, das der Nutzer angelegt wurde
                self.model.write_to_signup_json(user)
                raise Exception("Nutzer wurde Angelegt")
            
            except Exception as e:
                raise e

    #Die get_Json Funktion holt die ganzen Daten einer Json Datei
    def get_Json(self):
        Film_names = self.model.loaded_film_data
        print(Film_names)
        return Film_names
    
    #Die Funktion entnimmt sich alle Film Namen
    def get_Json_Film_Names(self):
        Film_names = self.model.get_json_data("film_names", None)
        return Film_names
    
    #Doe Funktion entnimmt alle User Namen der User Json
    def get_Json_User_Names(self):
        user_name = self.model.get_json_data("name", None)
        return user_name
    
    #Die Funktion entnimmt alle vorgeschlagenen Filme aus dem Algorythmus
    def get_Json_recommended_Film_Names(self, user):
        Film_names = self.model.get_recommendations(user)
        return Film_names
    
    def get_Json_recommended_Films_collaborative(self, user):
        Film_names = self.model.get_user_base_recommendations(user)
        #print(Film_names)
        return Film_names
    
    #Die Funktion entimmt alle gelikte Filmen aus der User json Datei
    def get_Json_user_Liked_Films(self, user):
        Film_names = self.model.get_json_data("favorite_movies",user)
        #print(Film_names)
        return Film_names
    
    #Die Funktion scheibt die ausgewählten Titel auf die Ausgewählte Datei der Listbox
    def write_to_Json(self,user,Listbox):
        try:
            #Den Index der Listbox zurückgeben, an dem Titel, den ich ausgewählt habe
            index = Listbox.curselection()
            #Den Namen des Indexes aus der Listbox zurückgeben
            liked_film = Listbox.get(index)
            #Jeden Film des eingeloggten Users durchgehen, welches er als Favorit gekenzeichnet hat.
            for movie in self.model.get_json_data("favorite_movies",user):
                #Überprüfen, das es den Film nicht gibt. Dalls doch, dann das Problem, das es den Film schon gibt, zurückgeben und den try Block unterbrechen
                if str(movie) == str(liked_film):
                    raise Exception("Film in der Liste schon vorhanden")
                
            self.model.write_to_json(user, liked_film)
            return liked_film
        
        #Falls ein Fehler vorliegt diesen melden und die Funktion unterbrechen
        except Exception as e:
            raise e

    #Die Funktion entfernt die ausgewählte datei der angegebenen Listbox
    def remove_from_list(self, user, Listbox):
        try:
            index = Listbox.curselection()
            filename = Listbox.get(index)
            self.model.removed_liked_films_from_jason(user, filename)
        
        except Exception as e:
            print(e)