import os
import json
import time
import subprocess
from datetime import datetime

# Configuration
INACTIVITY_LIMIT_SECONDS = 3600  # 1 heure
TRANSCRIBER_ACCOUNT = "transcriber"
SESSIONS_DIR = "/home/simon/gladys/openclaw/sessions"

def get_last_message_time(session_file):
    try:
        with open(session_file, 'r') as f:
            data = json.load(f)
            messages = data.get('messages', [])
            if not messages:
                return os.path.getmtime(session_file)
            
            # On cherche le timestamp du dernier message (format ISO ou ms)
            last_msg = messages[-1]
            ts = last_msg.get('ts')
            if ts:
                return ts / 1000 # On assume ms
    except:
        pass
    return os.path.getmtime(session_file)

def reset_session(session_key):
    print(f"Resetting session: {session_key}")
    # On utilise sessions_send pour envoyer la commande /new
    # session_key format: agent:account:userId
    cmd = [
        "openclaw", "sessions", "send",
        "--session", session_key,
        "--message", "/new"
    ]
    subprocess.run(cmd)

def main():
    if not os.path.exists(SESSIONS_DIR):
        return

    now = time.time()
    
    for filename in os.listdir(SESSIONS_DIR):
        if not filename.endswith(".json"):
            continue
            
        # Format attendu: agent_account_userId.json
        parts = filename.replace(".json", "").split("_")
        if len(parts) < 3:
            continue
            
        account = parts[1]
        if account != TRANSCRIBER_ACCOUNT:
            continue
            
        session_path = os.path.join(SESSIONS_DIR, filename)
        last_activity = get_last_message_time(session_path)
        
        if (now - last_activity) > INACTIVITY_LIMIT_SECONDS:
            session_key = f"agent:{parts[1]}:{parts[2]}"
            # On ne reset que si la session n'est pas déjà vide (plus de 1 message)
            try:
                with open(session_path, 'r') as f:
                    data = json.load(f)
                    if len(data.get('messages', [])) > 1:
                        reset_session(session_key)
            except:
                pass

if __name__ == "__main__":
    main()
