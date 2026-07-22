Collection App – Desktop-Programm
==================================

Einmalige Einrichtung
----------------------
1. Falls noch nicht vorhanden: Python installieren
   https://www.python.org/downloads/
   WICHTIG beim Installer: Haken bei "Add Python to PATH" setzen.

2. Diesen Ordner (collection-app) an diesem Ort belassen bzw. nicht mehr
   verschieben, da die Datenbank-Datei relativ zum Programm gespeichert wird.

Start
-----
Start.bat per Doppelklick oeffnen.
Beim allerersten Start dauert es einen Moment (pywebview wird installiert),
danach oeffnet sich das Programm sofort in einem eigenen Fenster.

Sammlungen / Franchises
------------------------
Die App ist nicht mehr auf eine einzige Serie festgelegt. In der Navigation
links ist "One Piece" als erste Sammlung bereits eingerichtet (mit den
Kategorien TCG Karten und Manga). Über "+ Neue Sammlung" lassen sich weitere
Franchises ergänzen (z.B. Dragon Ball, Pokémon, ...), jede mit eigenen
Kategorien über "+ Neue Kategorie" innerhalb der jeweiligen Sammlung.

Wo werden meine Daten gespeichert?
----------------------------------
In der Datei "collection_data.json" in genau diesem Ordner.
Diese Datei ist die eine Quelle der Wahrheit für deine Sammlung: sie bleibt
bei jedem Neustart und jedem zukünftigen Update des Programms erhalten,
unabhängig von Browser-Speicher-Problemen, wie sie in der Web-Version
auftreten konnten.

Backup / Umzug auf einen anderen PC
------------------------------------
- Über den "Export (JSON)"-Button in der App kannst du jederzeit eine
  Sicherungskopie an einem Ort deiner Wahl speichern.
- Über "Import (JSON)" kannst du eine solche Sicherung (oder die Datei
  collection_data.json von einem anderen PC) wieder einlesen.
- Alternativ: Kopiere einfach den ganzen Ordner (inkl. collection_data.json)
  auf einen anderen PC und starte dort ebenfalls Start.bat.

Bekannte Einschränkung
------------------------
Dieses Setup benötigt eine lokale Python-Installation. Es ist kein
fertiges .exe zum Weitergeben ohne Python. Bei Bedarf lässt sich daraus
später mit PyInstaller (auf einem Windows-Rechner ausgeführt) eine
eigenständige .exe bauen.

Web-Version
-----------
Die Datei "collection-tracker.html" in diesem Ordner ist die ursprüngliche
Browser-Version derselben App (funktioniert ohne Python, einfach
doppelklicken und im Browser öffnen). Sie speichert im Browser-Speicher
statt in einer Datei und ist daher weniger zuverlässig bei App-Updates als
das Desktop-Programm oben.

Als App auf dem Handy (Samsung Galaxy / Android) nutzen
--------------------------------------------------------
Voraussetzung: PC und Handy sind im selben WLAN.

1. Auf dem PC "Start-Server.bat" per Doppelklick öffnen und das Fenster
   offen lassen. Es zeigt eine Adresse wie:
     http://192.168.1.42:8765
   (beim allerersten Start dauert die Einrichtung kurz länger)

2. Auf dem Samsung Galaxy im selben WLAN Chrome öffnen (oder Samsung
   Internet) und genau diese Adresse eintippen.

3. App installieren:
   - Chrome: Menü (drei Punkte oben rechts) -> "App installieren" oder
     "Zum Startbildschirm hinzufügen".
   - Samsung Internet: Menü (drei Striche unten) -> "Seite hinzufügen zu"
     -> "Startbildschirm".

4. Ab jetzt liegt ein eigenes Icon auf dem Homescreen, die App öffnet
   sich ohne Browser-Leiste wie eine normale App.

Wichtig: Der PC mit laufendem Start-Server.bat muss beim Nutzen der
Handy-App eingeschaltet und im selben WLAN sein. Handy-App und
Desktop-Programm (Start.bat) greifen auf dieselbe Datei
collection_data.json zu und zeigen daher denselben Stand - Änderungen auf
dem einen Gerät erscheinen nach einem Neuladen auch auf dem anderen. Am PC
selbst lässt sich dieselbe Adresse auch unter http://localhost:8765 im
Browser öffnen.

Für Zugriff von unterwegs (außerhalb des Heim-WLANs) wäre zusätzlich
echtes Internet-Hosting nötig - bei Bedarf sag Bescheid, das lässt sich
nachrüsten.

Hinweis zum App-Icon: aus Zeit-/Rechtegründen ist das Icon ein selbst
gestaltetes, generisches Piraten-Symbol (Totenkopf) statt lizenzierter
Grafik. Kann bei Bedarf gegen ein eigenes Bild ausgetauscht werden
(icon.svg ersetzen).
