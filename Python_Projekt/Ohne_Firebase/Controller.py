import tkinter as tk
import View
import Model

class Controler():
    def __init__(self):
        user_db_path = r"Python_Projekt\Ohne_Firebase\users.json"
        films_db_path = r"Python_Projekt\Ohne_Firebase\Films.json"

        self.model = Model.Model(user_db_path, films_db_path)
        self.view = View.View(self)

        self.view.mainloop()
    
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

    def get_Json(self):
        Film_names = self.model.get_json()
        return Film_names
    
    def get_Json_Film_Names(self):
        Film_names = self.model.get_films_from_json()
        return Film_names

    def get_Json_User_Names(self):
        Film_names = self.model.get_names_from_json()
        return Film_names
    
    def get_Json_recommended_Film_Names(self, user):
        Film_names = self.model.get_recommendations(user)
        print(Film_names)
        return Film_names
    
    def get_Json_user_Liked_Films(self, user):
        Film_names = self.model.get_recommended_films_from_json(user)
        print(Film_names)
        return Film_names