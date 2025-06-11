import sys

def load(file):
    try:
        with open(file) as in_file:
            loaded_txt = in_file.read().lower().strip("").split('\n')
                
            return loaded_txt
        
    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
            file=sys.stderr)
        sys.exit(1)


import json

def get_names_from_json(filepath):
    names = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            for user in data:
                if isinstance(user, dict) and 'name' in user:
                    names.append(str(user['name']).lower())
                else:
                    print(f"Warnung: Ungültiges Benutzerobjekt gefunden: {user}")
        else:
            print(f"Fehler: Die JSON-Datei enthält keine Liste auf der obersten Ebene. Typ: {type(data)}")

    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden unter: {filepath}")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON-Format in der Datei: {filepath}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    return names
