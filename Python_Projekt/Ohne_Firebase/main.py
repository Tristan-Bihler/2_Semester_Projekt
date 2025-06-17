import Controller
"""
In der heutigen digitalen Welt sind Online-Dienste fester Bestandteil unseres Alltags.
Ob beim Einkaufen, Video-Streaming oder in sozialen Netzwerken - personalisierte Werbung ist auf unzählige Online-Plattformen kaum wegzudenken.
Hier liegt das Problem, denn wie finden Nutzer unter der Informationenflut im Netz genau das, was sie wirklich interessiert und ihren individuellen Vorlieben entspricht?
Die Antwort ist ein Empfehlungssystem.

Das Ziel unseres Projekts ist es, dieses Problem zu lösen und ein solches Empfehlungssystem zu entwickeln und zu implementieren.
Es soll in der Lage sein, basierend auf dem historischen Verhalten und den Präferenzen von Nutzern maßgeschneiderte Empfehlungen zu generieren und zu speichern.
Dies beinhaltet die Konzeption und Implementierung einer geeigneten Datenstruktur für Nutzerpräferenzen, sowie die Entwicklung eines Algorithmus zur Berechnung von Ähnlichkeiten zwischen Produkten.

Wir haben uns für die konkrete Entwicklung eines Empfehlungssystems für einen Streaming-Dienst entschieden. Hierfür muss zum Beispiel ein Weg gefunden werden, um herauszufinden welche Filme einem ähnlichen Genre angehören und ob diese dem Nutzer gefallen können oder eher nicht. 
Außerdem soll es eine Möglichkeit geben, dass Filme in einer Favoritenliste gespeichert werden könne und zusätzlich darauf Empfehlungen angezeigt werden.


Wichtig, das Projekt muss aus dem Ordner Abgaben geöffnet werden, und nicht aus einem anderen. Sonst kann der Compiler die Pfade der Datenbanken nicht finden.


In der Login-Übersicht kann sich der User unter „Login“ anmelden und unter „Registrieren“ einen Nutzer anlegen. Nach dem erfolgreichen Einloggen wird der Nutzer auf die Übersichtsseite weitergeleitet. Auf dieser kann der Nutzer auf der linken Seite die Filme sehen.

Nun kann der Nutzer einen Film auswählen. Die Applikation zeigt dann die Details zu diesem Film auf der unteren Seite der generellen Übersicht an. Hier kann der Film zur Favoritenliste hinzugefügt werden. Auf der rechten Seite aktualisieren sich dann die Filmempfehlungen basierend auf der eigenen Favoritenliste.

Nun kann der Nutzer oben rechts zur Favoritenseite wechseln und die Favoritenliste einsehen und gegebenfalls einzelne Filme entfernen. Zudem werden auf der rechten Seite Filme von ähnlichen Nutzerprofilen vorgeschlagen, welche wie gewohnt zur Favoritenliste hinzugefügt werden können.

Das Ausloggen erfolgt nach dem Beenden der Applikation.


Anmerkung:
Die Films.Json Liste wurde mit Daten der TMDB API ausgefüllt.
Die Applikation dient nur im Privaten sinne.
https://developer.themoviedb.org/reference/intro/getting-started
"""

if __name__ == "__main__":
    controler = Controller.Controller()