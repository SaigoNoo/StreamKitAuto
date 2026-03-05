import requests
import json
import random
import string
import time
import threading
import time as t


class StreamLabWS:
    def __init__(self, ip, port, token):
        self.ip = ip
        self.port = port
        self.token = token
        self.source_id = None
        self.base = f"http://{self.ip}:{self.port}/api"
        self.server_id = str(random.randint(1, 999)).zfill(3)
        self.session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self._msg_id = 1
        self._open_config()
        self._connect()
        self._start_heartbeat()

    def _open_config(self):
        with open(file='config.json', mode='r', encoding="utf-8") as f:
            self.source_id = json.load(f)['browser_id']

    def _connect(self, retries=3):
        if retries == 0:
            raise ConnectionError("❌ Impossible de se connecter après 3 tentatives")
        try:
            self._open_session()
            self._auth()
        except Exception as e:
            print("❌ Erreur:", e)
            time.sleep(2)
            self._connect(retries - 1)

    def _start_heartbeat(self):
        def beat():
            while True:
                time.sleep(25)  # toutes les 25 secondes
                try:
                    requests.post(f"{self.base}/{self.server_id}/{self.session_id}/xhr", timeout=5)
                except:
                    self._connect()

        t = threading.Thread(target=beat, daemon=True)
        t.start()

    def _open_session(self):
        print("\nConnexion au WebSocket...", end="")
        requests.post(f"{self.base}/{self.server_id}/{self.session_id}/xhr", timeout=5)
        print("✅")

    def _auth(self):
        print("Authentification...", end="")
        self._send("auth", {"resource": "TcpServerService", "args": [self.token]})
        self._poll()  # consomme le résultat
        print("✅")

    def _send(self, method, params):
        """Envoi d'une requête avec gestion automatique de reconnexion"""
        payload = json.dumps([json.dumps({
            "jsonrpc": "2.0",
            "id": self._msg_id,
            "method": method,
            "params": params
        })])
        self._msg_id += 1
        try:
            requests.post(f"{self.base}/{self.server_id}/{self.session_id}/xhr_send", data=payload, timeout=5)
        except Exception as e:
            print("⚠ Envoi échoué, tentative de reconnexion :", e)
            self._connect()
            self._send(method, params)  # réessaye après reconnexion

    def _poll(self):
        """Récupère les résultats, avec reconnexion si nécessaire"""
        try:
            r = requests.post(f"{self.base}/{self.server_id}/{self.session_id}/xhr", timeout=10)
            data = json.loads(json.loads(r.text[1:])[0])
            return data.get("result")
        except Exception as e:
            print("⚠ Poll échoué, tentative de reconnexion :", e)
            self._connect()
            return self._poll()  # réessaye après reconnexion

    def _send_only(self, method, params):
        """Envoi sans attendre de réponse"""
        payload = json.dumps([json.dumps({
            "jsonrpc": "2.0",
            "id": self._msg_id,
            "method": method,
            "params": params
        })])
        self._msg_id += 1
        try:
            requests.post(f"{self.base}/{self.server_id}/{self.session_id}/xhr_send", data=payload, timeout=5)
        except Exception as e:
            print("⚠ Envoi échoué, tentative de reconnexion :", e)
            self._connect()
            self._send_only(method, params)

    def _call(self, method, params, poll: bool = True):
        self._send(method, params)
        if poll:
            return self._poll()
        return None

    def list_scenes(self):
        print("Récupération des scènes...", end="")
        scenes = self._call("getScenes", {"resource": "ScenesService", "args": []})
        print("✅")
        print("\nVeuillez sélectionner la scène où se trouve le plugin vocal :")
        return scenes

    def set_source_property(self, value):
        unique_url = f"{value}&_t={int(t.time())}"
        self._call("setPropertiesFormData", {
            "resource": f"Source[\"{self.source_id}\"]",
            "args": [[{"name": "url", "value": unique_url}]]
        }, poll=False)
