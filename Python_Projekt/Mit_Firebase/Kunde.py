import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth # To manage users from the backend
import os

SERVICE_ACCOUNT_KEY_PATH = r'Python_Projekt\Mit_Firebase\shop-f1cbd-firebase-adminsdk-fbsvc-6aa034b2e7.json'

class Kunde:
    def __init__(self):

        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.auth = auth

        print("Firestore and Auth clients initialized.")
        

    def login(self, email_entry, password_entry):
        try:
            email = email_entry.get()
            password = password_entry.get()

            user = self.auth.sign_in_with_email_and_password(email, password)
            user_uid = user['localId'] # This is the authenticated user's UID
            user_id_token = user['idToken'] # This token is needed for authenticated DB access
            return user.auth, user_uid, user_id_token
        
        except:
            return Exception

    def get_produkts(self, user_uid, user_id_token):
        user_data = self.db.child("Shop").child(user_uid).get(user_id_token).val()

        return user_data

    def logout(self):
        self.auth.revoke_refresh_tokens(self.user)

    def sign_up(self, email, password):
        try:
            user = auth.create_user(
                email = email,
                password = password,
                display_name = email
            )
        except Exception as e:
            print(f"Error creating user: {e}")
            raise # Re-raise the exception for upstream handling


    def Einlkaufwagen_inhalt():
        pass