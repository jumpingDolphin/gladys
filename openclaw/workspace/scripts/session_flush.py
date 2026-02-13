import os
import json
import sys
from datetime import datetime

SESSIONS_DIR = "/home/simon/gladys/openclaw/sessions"
MEMORY_DIR = "/home/simon/gladys/openclaw/workspace/memory"

def flush_session(session_key):
    # Transformer la clé en nom de fichier
    filename = session_key.replace(":", "_") + ".json"
    session_path = os.path.join(SESSIONS_DIR, filename)
    
    if not os.path.exists(session_path):
        return f"Erreur : Session {session_path} introuvable."

    try:
        with open(session_path, 'r') as f:
            data = json.load(f)
            messages = data.get('messages', [])
            if not messages:
                return "Session vide, rien à flusher."

        # Préparer le contenu à envoyer au modèle pour résumé (via agent isolé plus tard ou ici en brut)
        # Pour ce script technique, on va juste extraire les derniers échanges
        summary_content = "\n".join([f"{m['role']}: {m.get('content', '')}" for m in messages[-20:] if m.get('content')])
        
        # On va créer un agent Turn isolé pour générer le résumé (plus propre)
        return summary_content
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(flush_session(sys.argv[1]))
