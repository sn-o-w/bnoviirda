# Imports
from clasa_si_analizare import TwitchBot
import variabile_globale as vg
from get_access_token import get_access_token
from get_user_id import get_user_id
from bottle import Bottle, run, route

# Creează o pagină web via Bottle pentru a-i da ping și a ține botul online
@route('/', 'GET')
def home():
    return "‎"

# Creează botul
def main():
    vg.bot_access_token = get_access_token()
    vg.bot_id = get_user_id(vg.bot_username)
    vg.owner_id = get_user_id(vg.owner)

    bot = TwitchBot(vg.bot_username, vg.bot_client_id, vg.bot_token, vg.owner)
    bot.start()

# Lansează codul
if __name__ == "__main__":
    # Rulează webserverul într-un thread separat
    from threading import Thread
    thread = Thread(target=lambda: run(host='0.0.0.0', port=3000))
    thread.start()

    # Pornește botul
    vg.initialize()
    main()