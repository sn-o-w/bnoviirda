# Imports
import os
from time import time
from dotenv import load_dotenv

# Variabile globale
def initialize():
    # Variabile blackjack on/off automat cand intra/iese dintr-un joc
    # blackjack off automat
    global bj_off_automat
    bj_off_automat = False


    # Variabile pentru jocul de ruleta
    # Indica momentul cand ruleta va deveni disponibila
    global timp_ruleta
    timp_ruleta = time()

    # Indica premiul de la ruleta
    global premiu_ruleta
    premiu_ruleta = 1000


    # Variabile pentru blackjack
    # Indica momentul cand blackjack-ul va deveni disponibil
    global timp_blackjack
    timp_blackjack = time()

    # Indica momentul cand pedeapsa de la blackjack se va produce
    global pedeapsa_blackjack
    pedeapsa_blackjack = time()

    # Indica user-ul de la blackjack
    global user_blackjack
    user_blackjack = None

    # Indica alegerea user-ului de la blackjack
    global alegere_blackjack
    alegere_blackjack = None

    # Indica miza user-ului de la blackjack
    global miza_blackjack
    miza_blackjack = None

    # Indica daca partida de blackjack a inceput sau nu
    global flag_start_blackjack
    flag_start_blackjack = False

    # Indica daca s-a tras un As sau nu la blackjack
    global flag_as_blackjack
    flag_as_blackjack = False

    # Indica daca trebuie verificat cati Vons are user-ul de la blackjack
    global flag_puncte_blackjack
    flag_puncte_blackjack = True

    # Indica numarul de Vons pe care-l are user-ul de la blackjack
    global puncte_temp_blackjack
    puncte_temp_blackjack = None

    # Indica totalul pe care user-ul il are la blackjack
    global total_blackjack
    total_blackjack = 0

    # Indica totalul botului
    global total_blackjack_bot
    total_blackjack_bot = 0

    # Indica cartile botului
    global carti_blackjack_bot
    carti_blackjack_bot = []

    global carti_blackjack_bot_final
    carti_blackjack_bot_final = ""


    # Variabile pentru jocul piatra, hartie, foarfeca
    # Indica momentul cand jocul va fi disponibil
    global timp_phf
    timp_phf = time()

    # Indica momentul cand pedeapsa de la joc va avea loc
    global pedeapsa_phf
    pedeapsa_phf = time()

    # Indica user-ul de la joc
    global user_phf
    user_phf = None

    # Indica alegerea user-ului de la joc
    global alegere_phf
    alegere_phf = None

    # Indica miza user-ului de la joc
    global miza_phf
    miza_phf = None

    # Indica daca trebuie verificat cati Vons are user-ul de la joc
    global flag_puncte_phf
    flag_puncte_phf = True

    # Indica cati Vons are user-ul de la joc
    global puncte_temp_phf
    puncte_temp_phf = None


    # Variabile pentru loto
    # Indica numarul castigator
    global numar_loto
    numar_loto = None

    # Indica premiul de la loto
    global premiu_loto
    premiu_loto = None


    # Variabile pentru grinch
    # Toti subs
    global all_subs
    all_subs = []

    # Toti plebs
    global all_plebs
    all_plebs = []

    # Indica momentul cand comanda grinch va fi disponibila
    global timp_grinch
    timp_grinch = time()


    # Variabila give flower
    # Indica momentul cand comanda va fi disponibila
    global timp_flower
    timp_flower = time()

    # Indica toti userii care au primit deja cel putin o floricica
    global all_flower
    all_flower = []


    # Variabila video random
    # Indica momentul cand video-ul random va fi disponibil
    global timp_video
    timp_video = time()


    # Variabila comanda cuminte
    # Indica momentul cand comanda va fi disponibila
    global timp_cuminte
    timp_cuminte = time()


    # Variabila intrebari
    # Indica intrebarile posibile
    global intrebari
    intrebari = ["facultate", "inaltime", "ani", "inceput", "zodie"]


    # Variabila Vons
    # Indica momentul cand toti userii din chat vor primi Vons
    global timp_puncte
    timp_puncte = time() + 600

    # Indica momentul cand mesajul automat de la bot cu link-urile cu informatii despres Vons si comenzi vor fi trimise
    global timp_ajutor
    timp_ajutor = time() + 1800

    # Indica toti userii care au scris cel putin un mesaj in chat in ultimele X minute
    global chat
    chat = []

    # Indica toti userii care au scris cel putin un mesaj in chat de cand a inceput stream-ul
    global all
    all = []

    # Indica toti userii din baza de date
    global data
    data = []

    # Indica numele botilor care nu vor primi Vons
    global evit
    evit = ['testingvob', 'Nightbot', 'StreamElements']


    # Variabile games on/off
    # Indica daca blackjack-ul e pornit sau oprit
    global on_bj
    on_bj = False

    # Indica daca ruleta e pornita sau oprita
    global on_ruleta
    on_ruleta = True

    # Indică daca jocul de piatră, hârtie, foarfecă e oprit sau pornit
    global on_phf
    on_phf = True


    # Troll
    global troll_emotes
    troll_emotes = ["odoamne3Head", "odoamne4Head", "odoamne5Head", "odoamneW", "odoamnePOG", "odoamneFlag",
                    "odoamneL", "odoamneHeart", "odoamneGASP", "odoamneSip", "odoGOOD"]


    # Variables for the owner of the channel and the bot
    # Indicates the streamer's username
    global owner
    owner = os.environ['OWNER']  # Here you have to put the channel the bot will connect to (variable type: string. Example: "Twitch")
    owner = owner.lower()

    # Indicates the streamer's ID
    global owner_id
    owner_id = None      # Here the streamer's ID will be automatically put

    # Indicates the bot's username
    global bot_username
    bot_username = os.environ['BOT_USERNAME']      # Here you have to put the bot's username
    bot_username = bot_username.lower()

    # Indicates the bot's ID
    global bot_id
    bot_id = None       # Here the bot's ID will be automatically put

    # Indicates the bot's OATH token
    global bot_token
    bot_token = os.environ['BOT_OATH_TOKEN']   # Here you have to put the OATH token of the bot

    # Indicates the bot's user access token
    global bot_access_token
    bot_access_token = None  # Here the user access token of the bot will be automatically put

    # Indicates the bot's client ID
    global bot_client_id
    bot_client_id = os.environ['BOT_CLIENT_ID']   # Here you have to put the client ID of the bot

    # Indicates the bot's client secret
    global bot_client_secret
    bot_client_secret = os.environ['BOT_CLIENT_SECRET']   # Here you have to put the client secret of the bot

    # Indicates the bot's authorization code
    global bot_authorization_code
    bot_authorization_code = os.environ["BOT_AUTH_CODE"]  # Here you have to put the authorization code of the bot (variable type: string) (Example: "1234q567sfs890")