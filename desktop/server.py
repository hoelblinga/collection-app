"""
Collection App - Lokaler Server fuer Handy-Zugriff

Startet einen kleinen Webserver, der die App (index.html) sowie eine
einfache API (/api/data) im lokalen WLAN bereitstellt. Damit kann das
Handy dieselbe index.html oeffnen wie das Desktop-Programm und liest/
schreibt dieselbe Datei "collection_data.json" - Desktop und
Handy teilen sich also denselben Sammlungs-Stand.

Wichtig: Dieser Server muss laufen, waehrend die App auf dem Handy
genutzt wird, und PC + Handy muessen im selben WLAN sein.
"""

import http.server
import json
import os
import socket
import time
import urllib.error
import urllib.request

PORT = 8765


def app_dir():
    return os.path.dirname(os.path.abspath(__file__))


DATA_FILE = os.path.join(app_dir(), "collection_data.json")

# Kartendatenbank (One Piece TCG) ueber die oeffentliche optcgapi.com-API.
# Wird lokal zwischengespeichert (24h) - teilt sich die Cache-Datei mit dem
# Desktop-Programm (app.py), falls beide auf demselben PC laufen.
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


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=app_dir(), **kwargs)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/data":
            content = ""
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print("Fehler beim Laden:", e)
            self._send_json({"data": content})
            return
        if self.path == "/api/tcgcards":
            self._send_json(fetch_tcg_cards())
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/data":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                payload = json.loads(body)
                data_str = payload.get("data", "")
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    f.write(data_str)
                self._send_json({"ok": True})
            except Exception as e:
                print("Fehler beim Speichern:", e)
                self._send_json({"ok": False, "error": str(e)}, status=400)
            return
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # weniger Konsolen-Ausgabe


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def main():
    ip = local_ip()
    print("=" * 56)
    print(" Collection App - lokaler Server")
    print("=" * 56)
    print(f" Auf dem Handy (im selben WLAN) im Browser oeffnen:")
    print(f"   http://{ip}:{PORT}")
    print()
    print(" Dieses Fenster/den Server laufen lassen, solange die")
    print(" App auf dem Handy genutzt werden soll.")
    print(" Beenden mit Strg+C oder Fenster schliessen.")
    print("=" * 56)
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
