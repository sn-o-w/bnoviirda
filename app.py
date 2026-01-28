import os, requests, signal, sys, time
from datetime import datetime, timedelta
import variabile_globale as vg
from clasa_si_analizare import TwitchBot
from get_user_id import get_user_id

CONFIG_PATH = "config.txt"

def load_config(config_path: str) -> dict:
    # Încarcă variabilele din config.txt într-un dicționar.
    config = {}
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Nu găsesc fișierul {config_path}!")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignoră liniile goale și comentariile
            if not line or line.startswith('#'):
                continue
            
            # Separă cheia de valoare
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Elimină ghilimelele dacă există
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                config[key] = value
    
    return config

def save_config(config_path: str, key: str, value: str) -> None:
    # Actualizează o variabilă în config.txt.
    lines = []
    key_found = False
    
    # Citește fișierul existent
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Actualizează valoarea existentă sau adaugă-o
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f'{key}="{value}"\n'
            key_found = True
            break
    
    # Dacă cheia nu există, adaug-o la sfârșitul fișierului
    if not key_found:
        lines.append(f'{key}="{value}"\n')
    
    # Scrie înapoi în fișier
    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def set_env_from_config(config: dict) -> None:
    """Setează variabilele de mediu din dicționarul config."""
    for key, value in config.items():
        os.environ[key] = value

def main() -> None:
    # Încarcă variabilele din config.txt
    config = load_config(CONFIG_PATH)
    
    # Setează variabilele de mediu pentru ca modulele următoare să le poată citi
    set_env_from_config(config)
    
    # Încarcă variabilele globale
    vg.initialize()
    
    # Rulează ping pentru prelungirea access tokenului prin intermediul refresh tokenului
    url = f"https://twitchtokengenerator.com/api/refresh/{vg.bot_refresh_token}"
    try:
        data = requests.get(url, timeout=(3, 10)).json()
        token = data.get("token")
        if token:
            print("Ping reușit pe refresh token.")
            vg.bot_access_token = token
            
            # Salvează noul token în config.txt
            save_config(CONFIG_PATH, "BOT_ACCESS_TOKEN", token)
            
            # Actualizează și variabila de mediu
            os.environ["BOT_ACCESS_TOKEN"] = token
    except Exception as e:
        print("Ping eșuat:", e)
    
    # Pornește botul
    vg.bot_id = get_user_id(vg.bot_username)
    vg.owner_id = get_user_id(vg.owner)
    bot = TwitchBot(
        vg.bot_username,
        vg.bot_client_id,
        vg.bot_access_token,
        vg.owner
    )
    bot.start()

if __name__ == "__main__":
    main()