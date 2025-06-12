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
    
    def signup(self, signup_Entry):
            #Es können mehrere gleiche benutzer exestieren, muss gefixt werden!!!
            #users = self.get_Json_User_Names()
            user = signup_Entry.get()
            user = user.strip().lower()
            self.model.write_to_signup_json(user)


    def get_Json(self):
        Film_names = self.model.loaded_film_data
        return Film_names
    
    def get_Json_Film_Names(self):
        Film_names = self.model.get_films_from_json()
        return Film_names

    def get_Json_User_Names(self):
        Film_names = self.model.get_names_from_json()
        return Film_names
    
    def get_Json_recommended_Film_Names(self, user):
        Film_names = self.model.get_recommendations(user)
        return Film_names
    
    def get_Json_user_Liked_Films(self, user):
        Film_names = self.model.get_liked_films_from_jason(user)
        return Film_names
    
    def write_to_Json(self,user,Listbox):
        index = Listbox.curselection()
        liked_film = Listbox.get(index)
        self.model.write_to_json(user, liked_film)
    
    def remove_from_list(self, user, Listbox):
        index = Listbox.curselection()
        filename = Listbox.get(index)
        self.model.removed_liked_films_from_jason(user, filename)