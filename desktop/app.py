"""
Collection App - Desktop-Programm

Zeigt die vorhandene Web-App (index.html) in einem echten Programmfenster an
(ueber pywebview, nutzt WebView2 unter Windows). Der Sammlungs-Stand wird
nicht mehr im Browser-Speicher gehalten, sondern direkt in einer JSON-Datei
neben diesem Programm gespeichert. Das behebt das Problem, dass der Besitz-
Stand bei App-Updates oder Browser-Speicher-Resets verloren ging.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

import webview


def app_dir():
    """Ordner, in dem das Programm (bzw. das Skript) liegt."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


DATA_FILE = os.path.join(app_dir(), "collection_data.json")

# Kartendatenbank (One Piece TCG) ueber die oeffentliche optcgapi.com-API.
# Wird lokal zwischengespeichert (24h), damit nicht bei jedem Seitenaufruf neu
# abgefragt wird - schont die API und funktioniert auch offline mit altem Stand.
TCG_CACHE_FILE = os.path.join(app_dir(), "tcg_cards_cache.json")
TCG_CACHE_TTL = 24 * 60 * 60  # 24 Stunden
TCG_API_URL = "https://optcgapi.com/api/allSetCards/"


def read_tcg_cache():
    if os.path.exists(TCG_CACHE_FILE):
        try:
            with open(TCG_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def write_tcg_cache(cards, fetched_at):
    try:
        with open(TCG_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"cards": cards, "fetched_at": fetched_at}, f)
    except Exception as e:
        print("Fehler beim Schreiben des Karten-Caches:", e)


def fetch_tcg_cards():
    """Liefert die One-Piece-TCG-Kartendaten, aus dem Cache falls frisch genug,
    sonst neu von optcgapi.com abgerufen (server-seitig, da die API direkte
    Browser-Anfragen mit Origin-Header blockiert)."""
    cached = read_tcg_cache()
    if cached is not None:
        age = time.time() - cached.get("fetched_at", 0)
        if age < TCG_CACHE_TTL:
            return {"cards": cached["cards"], "cached": True, "fetchedAt": cached["fetched_at"]}
    try:
        req = urllib.request.Request(TCG_API_URL, headers={"User-Agent": "collection-app/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
        cards = json.loads(raw)
        fetched_at = time.time()
        write_tcg_cache(cards, fetched_at)
        return {"cards": cards, "cached": False, "fetchedAt": fetched_at}
    except Exception as e:
        print("Fehler beim Abruf der Karten-API:", e)
        if cached is not None:
            return {"cards": cached["cards"], "cached": True, "fetchedAt": cached.get("fetched_at"), "stale": True}
        return {"cards": [], "error": str(e)}


class Api:
    def load_data(self):
        """Liest den gespeicherten Sammlungs-Stand aus der JSON-Datei."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print("Fehler beim Laden:", e)
        return ""

    def save_data(self, json_str):
        """Speichert den aktuellen Sammlungs-Stand in die JSON-Datei."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                f.write(json_str)
            return True
        except Exception as e:
            print("Fehler beim Speichern:", e)
            return False

    def export_data(self, json_str, suggested_name):
        """Oeffnet einen 'Speichern unter'-Dialog und schreibt die gewaehlte Datei."""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG, save_filename=suggested_name
            )
            if not result:
                return False
            path = result if isinstance(result, str) else result[0]
            with open(path, "w", encoding="utf-8") as f:
                f.write(json_str)
            return True
        except Exception as e:
            print("Fehler beim Export:", e)
            return False

    def get_tcg_cards(self):
        """Liefert alle One-Piece-TCG-Kartendaten (Name, Set, Preis, Bild, ...)
        als JSON-String an die Web-Oberflaeche."""
        return json.dumps(fetch_tcg_cards())

    def import_data(self):
        """Oeffnet einen Datei-Auswahl-Dialog und gibt den Dateiinhalt zurueck."""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG,
                allow_multiple=False,
                file_types=("JSON Dateien (*.json)", "Alle Dateien (*.*)"),
            )
            if not result:
                return None
            path = result[0] if isinstance(result, (list, tuple)) else result
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("Fehler beim Import:", e)
            return None


def main():
    api = Api()
    html_path = os.path.join(app_dir(), "index.html")
    webview.create_window(
        "Collection App",
        html_path,
        js_api=api,
        width=1280,
        height=820,
        min_size=(960, 620),
    )
    webview.start()


if __name__ == "__main__":
    main()
