* Welches Konzept will ich nutzen für die Fehler? -> Erster Impuls: Keine Abbrüche am Rand, Businesslogik handhabt das Problem


Programmablauf

Programm startet das erste Mal/ohne Parameter
|
--- DB existiert: Ausgabe des Standes
|
--- DB fehlt: DB fehlt

Programm startet mit Zeitparameter
|
--- DB existiert: Stunden werden verrechnet, Eingaben geprüft
|


store status und store inhalt trennen



---
logging strukturieren (logging-prinzipien festlegen)
return fuckup aufräumen
business-logik in store_handler etablieren
