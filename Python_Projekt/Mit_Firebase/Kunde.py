import pyrebase
import os


class Kunde:
    def __init__(self):

        firebaseConfig = {
            "apiKey": "AIzaSyBdatneRnVomArbti6kNruyk88Xi5Ac2Ys",
            "authDomain": "shop-f1cbd.firebaseapp.com",
            "projectId": "shop-f1cbd",
            "storageBucket": "shop-f1cbd.firebasestorage.app",
            "messagingSenderId": "340216273962",
            "appId": "1:340216273962:web:54022052951bbb678c7753",
            "measurementId": "G-C3KETBC0B2",
            "databaseURL": "https://shop-f1cbd-default-rtdb.europe-west1.firebasedatabase.app/"
        }

        self.fb = pyrebase.initialize_app(firebaseConfig)
        self.auth = self.fb.auth()

        print("Firestore and Auth clients initialized.")
        

    def login(self, email, password):

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            print(f"Successfully logged in user: {user['email']}")
            print("User data:", user)
            # The 'user' object contains 'idToken', 'refreshToken', 'localId' (UID), etc.
            return user
        
        except Exception as e:
            print(f"Login failed: {e}")
            # You can parse the error for more specific messages
            if "EMAIL_NOT_FOUND" in str(e):
                print("Error: Email not found.")
            elif "INVALID_PASSWORD" in str(e):
                print("Error: Invalid password.")
            elif "USER_DISABLED" in str(e):
                print("Error: User account is disabled.")
            else:
                print(f"An unexpected error occurred: {e}")
        return None


    def get_produkts(self, user_uid, user_id_token):
        user_data = self.db.child("Shop").child(user_uid).get(user_id_token).val()

        return user_data

    def logout(self):
        self.auth.revoke_refresh_tokens(self.user)

    def sign_up(self, email, password):
        pass