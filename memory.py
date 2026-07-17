import json
import os

class MemoryManager:
    """Gestisce la memoria persistente di Jarvis."""
    def __init__(self, filename="jarvis_memory.json"):
        self.filename = filename
        # Crea il file se non esiste
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def salva_ricordo(self, categoria, contenuto):
        """Salva un'informazione nuova nella memoria."""
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            data.append({"categoria": categoria, "contenuto": contenuto})
            f.seek(0)
            json.dump(data, f, indent=4)

    def leggi_tutta_la_memoria(self):
        """Jarvis legge i ricordi per avere contesto."""
        with open(self.filename, 'r') as f:
            return json.dumps(json.load(f))
