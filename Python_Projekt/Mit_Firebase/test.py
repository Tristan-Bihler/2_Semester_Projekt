import empyrebase

# Make sure to replace these with your actual Firebase project configuration
config = {
    "apiKey": "AIzaSyBdatneRnVomArbti6kNruyk88Xi5Ac2Ys",
    "authDomain": "shop-f1cbd.firebaseapp.com",
    "projectId": "shop-f1cbd",
    "storageBucket": "shop-f1cbd.firebasestorage.app",
    "messagingSenderId": "340216273962",
    "appId": "1:340216273962:web:54022052951bbb678c7753",
    "measurementId": "G-C3KETBC0B2",
    "databaseURL": "https://shop-f1cbd-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = empyrebase.initialize_app(config)
firestore_client = firebase.firestore()

# --- Corrected ways to create documents using empyrebase ---

# 1. Creating a document with an auto-generated ID (similar to .add() in other SDKs)
#    You provide the collection path and the data.
#    empyrebase's .add() method directly accepts the collection path and data.
try:
    data_for_new_doc = {"status": "pending", "createdAt": firestore_client.SERVER_TIMESTAMP}
    # For auto-generated ID, you typically provide the collection path and data
    # The return value might be slightly different; often it returns a dictionary
    # including the name (full path) of the created document.
    response_add = firestore_client.add("messages", data_for_new_doc)
    
    # Empyrebase's add method usually returns the name (full path) of the created document
    # You might need to parse this name to get the ID.
    # Example: 'projects/YOUR_PROJECT_ID/databases/(default)/documents/messages/auto_generated_id_here'
    # The last segment is the ID.
    created_doc_full_path = response_add.get('name', 'N/A')
    auto_generated_id = created_doc_full_path.split('/')[-1] if 'messages/' in created_doc_full_path else 'N/A'
    
    print(f"Document created with auto-generated ID: {auto_generated_id}")
    print(f"Full response for add: {response_add}")
except Exception as e:
    print(f"Error creating auto-generated document: {e}")


# 2. Creating an empty document with a specific ID (using .set())
#    You provide the full document path (collection/document_id) and the data.
#    To make it "empty," you pass an empty dictionary.
doc_id_specific_empty = "my_specific_empty_doc"
doc_path_specific_empty = f"empty_docs/{doc_id_specific_empty}"
try:
    firestore_client.set(doc_path_specific_empty, {})
    print(f"Empty document '{doc_id_specific_empty}' created in 'empty_docs' collection.")
except Exception as e:
    print(f"Error creating specific empty document: {e}")


# 3. Creating a document with explicitly empty/null fields (using .set())
doc_id_with_empty_fields = "user_profile_123"
doc_path_with_empty_fields = f"user_profiles/{doc_id_with_empty_fields}"
user_data = {
    "name": "",
    "email": None, # Will be stored as null in Firestore
    "preferences": {},
    "tags": []
}
try:
    firestore_client.set(doc_path_with_empty_fields, user_data)
    print(f"Document '{doc_id_with_empty_fields}' created with empty/null fields in 'user_profiles'.")
except Exception as e:
    print(f"Error creating document with empty fields: {e}")

# 4. Updating an existing document (using .update())
#    Similar to set, but only updates specified fields.
existing_doc_id = "my_specific_empty_doc" # Assuming this was created above
existing_doc_path = f"empty_docs/{existing_doc_id}"
update_data = {"status": "processed"}
try:
    firestore_client.update(existing_doc_path, update_data)
    print(f"Document '{existing_doc_id}' updated with 'status: processed'.")
except Exception as e:
    print(f"Error updating document: {e}")


# --- Authentication consideration (if your rules require it) ---
# If your Firestore Security Rules require authentication for write operations,
# you'll first need to sign in a user and then pass their ID token to the
# firestore client when initializing it.

# auth = firebase.auth()
# try:
#     user = auth.sign_in_with_email_and_password("test@example.com", "password123")
#     print(f"User signed in: {user['email']}")
#     # Re-initialize firestore client with the user's ID token
#     firestore_client_authenticated = firebase.firestore(auth_id=user['idToken'])
#
#     # Now use firestore_client_authenticated for operations that require auth
#     firestore_client_authenticated.set("authenticated_data/my_doc", {"data": "from authenticated user"})
#     print("Authenticated document created.")
#
# except Exception as e:
#     print(f"Authentication error: {e}")