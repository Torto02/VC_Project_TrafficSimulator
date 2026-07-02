import json
import os

class Config:
    def __init__(self, file_path="config.json"):
        self.data = {}
        self.load(file_path)

    def load(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.data = json.load(f)
            print(f"[Config] File {file_path} caricato con successo.")
        else:
            print(f"[Config] Avviso: File {file_path} non trovato. Verranno usati i valori di default hardcoded.")

    def get(self, key_path, default=None):
        """
        Permette di accedere ai dati nidificati. Es: get('gui.width', 1280)
        """
        keys = key_path.split('.')
        val = self.data
        try:
            for k in keys:
                val = val[k]
            return val
        except KeyError:
            return default