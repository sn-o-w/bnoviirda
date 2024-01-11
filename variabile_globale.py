# Imports
import os
from time import time
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(env_var_name):
    value = os.environ.get(env_var_name)

    if not value:
        print(f'Nicio variabilă definită în sistem sau în fișierul .env pentru {env_var_name}, se verifică config.txt.')
        try:
            with open("config.txt", "r") as config_file:
                for line in config_file:
                    if line.startswith(f"{env_var_name}="):
                        value = line.strip().split("=")[1].strip('"\n')
                        break
        except FileNotFoundError:
            print(f'Avertisment: {env_var_name} nu a fost găsit în config.txt.')

    return value

# Variabile globale
def initialize():
    # Variabile blackjack on/off automat când intră/iese dintr-un joc
    # blackjack off automat
    global bj_off_automat
    bj_off_automat = False


    # Variabile pentru jocul de ruletă
    # Indică momentul când ruleta va deveni disponibilă
    global timp_ruleta
    timp_ruleta = time()

    # Indică premiul de la ruletă
    global premiu_ruleta
    premiu_ruleta = 1000


    # Variabile pentru blackjack
    # Indică momentul când blackjackul va deveni disponibil
    global timp_blackjack
    timp_blackjack = time()

    # Indică momentul când pedeapsa de la blackjack va avea loc
    global pedeapsa_blackjack
    pedeapsa_blackjack = time()

    # Indică userul de la blackjack
    global user_blackjack
    user_blackjack = None

    # Indică alegerea userului de la blackjack
    global alegere_blackjack
    alegere_blackjack = None

    # Indică miza userului de la blackjack
    global miza_blackjack
    miza_blackjack = None

    # Indică dacă partida de blackjack a început sau nu
    global flag_start_blackjack
    flag_start_blackjack = False

    # Indică dacă s-a tras un as sau nu la blackjack
    global flag_as_blackjack
    flag_as_blackjack = False

    # Indică dacă trebuie verificat câți Vons are userul de la blackjack
    global flag_puncte_blackjack
    flag_puncte_blackjack = True

    # Indică numărul de Vons pe care îl are userul de la blackjack
    global puncte_temp_blackjack
    puncte_temp_blackjack = None

    # Indică totalul pe care îl are userul de la blackjack
    global total_blackjack
    total_blackjack = 0

    # Indică totalul botului
    global total_blackjack_bot
    total_blackjack_bot = 0

    # Indică cărțile botului
    global carti_blackjack_bot
    carti_blackjack_bot = []

    global carti_blackjack_bot_final
    carti_blackjack_bot_final = ""


    # Variabile pentru jocul piatră, hârtie, foarfecă
    # Indică momentul când jocul va deveni disponibil
    global timp_phf
    timp_phf = time()

    # Indică momentul când pedeapsa de la joc va avea loc
    global pedeapsa_phf
    pedeapsa_phf = time()

    # Indică userul de la joc
    global user_phf
    user_phf = None

    # Indică alegerea userului de la joc
    global alegere_phf
    alegere_phf = None

    # Indică miza userului de la joc
    global miza_phf
    miza_phf = None

    # Indică dacă trebuie verificat câți Vons are userul de la joc
    global flag_puncte_phf
    flag_puncte_phf = True

    # Indică câți Vons are userul de la joc
    global puncte_temp_phf
    puncte_temp_phf = None


    # Variabile pentru loto
    # Indică numărul câștigător
    global numar_loto
    numar_loto = None

    # Indică premiul de la loto
    global premiu_loto
    premiu_loto = None


    # Variabile pentru grinch
    # Toți subs
    global all_subs
    all_subs = []

    # Toți plebs
    global all_plebs
    all_plebs = []

    # Indică momentul când comanda a început
    global timp_grinch
    timp_grinch = time()


    # Variabila pentru !flower
    # Indică momentul când comanda a început
    global timp_flower
    timp_flower = time()

    # Indică toți userii care au primit deja cel puțin o floricică
    global all_flower
    all_flower = []


    # Variabila pentru video random
    # Indică momentul când videoul random va fi disponibil
    global timp_video
    timp_video = time()


    # Variabila pentru !cuminte
    # Indică momentul când comanda a început
    global timp_cuminte
    timp_cuminte = time()


    # Variabila pentru întrebări
    # Indică întrebările posibile
    global intrebari
    intrebari = ["facultate", "inaltime", "ani", "inceput", "zodie"]


    # Variabila pentru Vons
    # Indică momentul când toți userii din chat vor primi Vons
    global timp_puncte
    timp_puncte = time() + 600

    # Indică momentul când mesajul automat de la bot cu linkurile cu informații despre Vons și comenzi vor fi trimise
    global timp_ajutor
    timp_ajutor = time() + 1800

    # Indică toți userii care au scris cel puțin un mesaj în chat in ultimele X minute
    global chat
    chat = []

    # Indică toți userii care au scris cel puțin un mesaj în chat de când a început streamul
    global all
    all = []

    # Indică toți userii din baza de date
    global data
    data = []

    # Indică numele boților care nu vor primi Vons
    global evit
    evit = ['testingvonb', 'Nightbot', 'StreamElements']


    # Variabile de on/off dedicate game-urilor
    # Indică dacă blackjackul e pornit sau oprit
    global on_bj
    on_bj = False

    # Indică dacă ruleta e pornită sau oprită
    global on_ruleta
    on_ruleta = True

    # Indică dacă jocul de piatră, hârtie, foarfecă e oprit sau pornit
    global on_phf
    on_phf = True


    # Troll
    global troll_emotes
    troll_emotes = ["odoamne3Head", "odoamne4Head", "odoamne5Head", "odoamneW", "odoamnePOG", "odoamneFlag",
                    "odoamneL", "odoamneHeart", "odoamneGASP", "odoamneSip", "odoGOOD"]


    # Variabile pentru proprietarul canalului și al botului
    # Indică username-ul streamerului
    global owner
    owner = get_env_variable('OWNER')
    owner = owner.lower()

    # Indică ID-ul streamerului
    global owner_id
    owner_id = None

    # Indică username-ul botului
    global bot_username
    bot_username = get_env_variable('BOT_USERNAME')
    bot_username = bot_username.lower()

    # Indică ID-ul botului
    global bot_id
    bot_id = None

    # Indică tokenul OATH al botului
    global bot_token
    bot_token = get_env_variable('BOT_OATH_TOKEN')

    # Indică tokenul de user access pentru bot
    global bot_access_token
    bot_access_token = None

    # Indică valoarea botului pentru client ID
    global bot_client_id
    bot_client_id = get_env_variable('BOT_CLIENT_ID')

    # Indică valoarea botului pentru client secret
    global bot_client_secret
    bot_client_secret = get_env_variable('BOT_CLIENT_SECRET')

    # Indică valoarea botului pentru authorization code
    global bot_authorization_code
    bot_authorization_code = get_env_variable('BOT_AUTH_CODE')