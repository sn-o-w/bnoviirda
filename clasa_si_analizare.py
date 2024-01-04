# Imports
import irc.bot, requests
import variabile_globale as vg
from time import time
from jocuri.jocuri_ruleta import ruleta
from jocuri.jocuri_phf import phf, penalizare_phf
from jocuri.jocuri_loto import mods_loto, loto_castigat
from jocuri.jocuri_blackjack import blackjack, penalizare_blackjack
from jocuri.jocuri_activare import on, off, on_auto, off_auto
from comenzi_globale.love import love
from comenzi_globale.cuminte import cuminte
from comenzi_globale.grinch import grinch
from comenzi_globale.flower import flower, top_10_flower
from comenzi_globale.troll import troll
from comenzi_globale.video_random import video_random
from comenzi_globale.comenzi_help import comenzi, ajutor, botplay, new_user
from comenzi_mods.coinflip import mods_coinflip
from comenzi_mods.categorie import mods_schimba_categoria
from comenzi_mods.intrebari import intrebari
from puncte import puncte_chat, puncte_user, mods_puncte, schimb_puncte

# Clasa TwitchBot (definirea acțiunilor botului)
class TwitchBot(irc.bot.SingleServerIRCBot):

    # Botul se conectează la Twitch
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        self.channel_id = vg.owner_id

        # Creează conexiunea IRC pentru bot
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    # Botul se conectează în chatul canalului
    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # Specifică capabilitățile dorite pentru bot
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print('Joined ' + self.channel)
        # c.privmsg(self.channel, "peepoHey")

    # Botul analizează mesajele din chat
    def on_pubmsg(self, c, e):

        # Informații despre user
        tags = {}
        for i in range(len(e.tags)):
            tags[e.tags[i]["key"]] = e.tags[i]["value"]

        # Verifică ce comandă e
        # Număr la loto
        if len(e.arguments[0].split()) == 1 and vg.numar_loto is not None:
            try:
                incercare = int(e.arguments[0].split()[0])
                if incercare == vg.numar_loto:
                    jucator = tags["display-name"]
                    loto_castigat(self, jucator)
            except:
                pass

        # Add chatter
        if tags["display-name"] not in vg.chat and tags["display-name"] not in vg.evit:
            vg.chat.append(tags["display-name"])

        if tags["display-name"] not in vg.all and tags["display-name"] not in vg.evit:
            vg.all.append(tags["display-name"])

        # Blackjack on/off automat
        # Off
        if vg.bj_off_automat and vg.on_bj and vg.user_blackjack is None:
            off_auto(self)

        if "The stream game has been updated to: Marbles On Stream" in e.arguments[0]:
            if vg.on_bj and vg.user_blackjack is None:
                off_auto(self)

            elif vg.on_bj and vg.user_blackjack is not None:
                vg.bj_off_automat = True

        elif "The stream game has been updated to: Just Chatting" in e.arguments[0]:
            if vg.on_bj and vg.user_blackjack is None:
                off_auto(self)

            elif vg.on_bj and vg.user_blackjack is not None:
                vg.bj_off_automat = True

        elif "The stream game has been updated to: Food & Drink" in e.arguments[0]:
            if vg.on_bj and vg.user_blackjack is None:
                off_auto(self)

            elif vg.on_bj and vg.user_blackjack is not None:
                vg.bj_off_automat = True

        elif "The stream game has been updated to: Travel & Outdoors" in e.arguments[0]:
            if vg.on_bj and vg.user_blackjack is None:
                off_auto(self)

            elif vg.on_bj and vg.user_blackjack is not None:
                vg.bj_off_automat = True

        # On
        elif "The stream game has been updated to: " in e.arguments[0] and not vg.on_bj:
            on_auto(self)

        # Mesaj ajutor Vons automat
        if time() > vg.timp_ajutor:
            user = None
            alt_user = "@chat"
            ajutor(self, user, alt_user)

        # Puncte pentru chat
        if time() > vg.timp_puncte:
            puncte_chat(self, vg.chat)

        # Pedeapsă piatră, hârtie, foarfecă
        if vg.user_phf is not None and time() > vg.pedeapsa_phf:
            penalizare_phf(self, vg.user_phf, vg.miza_phf)

        # Pedeapsă blackjack
        if vg.user_blackjack is not None and time() > vg.pedeapsa_blackjack:
            penalizare_blackjack(self, vg.user_blackjack, vg.miza_blackjack)

        '''
        # Troll
        for emote in vg.troll_emotes:
            if emote in e.arguments[0]:
                user = tags["display-name"]
                troll(self, user)
                break
        '''

        # Mesaj pentru userii noi din chat
        if tags["first-msg"] == "1":
            user = tags["display-name"]
            new_user(self, user)

        # Verificare dacă userul e subscriber
        if tags["subscriber"] == "1" and tags["display-name"] not in vg.all_subs \
                and tags["display-name"] not in vg.evit:

            user = tags["display-name"]
            if user in vg.all_plebs:
                vg.all_plebs.remove(user)
            vg.all_subs.append(user)

        # Verificare dacă userul nu e subscriber
        elif tags["subscriber"] == "0" and tags["display-name"] not in vg.all_plebs \
                and tags["display-name"] not in vg.evit:

            user = tags["display-name"]
            if user in vg.all_subs:
                vg.all_subs.remove(user)
            vg.all_plebs.append(user)

        # Comenzi globale
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]

            # Piatră, hârtie, foarfecă când o partidă e în curs
            if vg.user_phf == tags["display-name"] and cmd == "joc" and vg.on_phf:
                try:
                    temp = e.arguments[0].split()
                    vg.alegere_phf = temp[1]
                except:
                    pass
                phf(self, vg.alegere_phf, vg.user_phf, vg.miza_phf)

            # Piatră, hârtie, foarfecă cand se începe o partidă
            elif cmd == "joc" and vg.user_phf is None and vg.on_phf:
                vg.user_phf = tags["display-name"]
                try:
                    temp = e.arguments[0].split()
                    vg.alegere_phf = temp[1]
                    vg.miza_phf = temp[2]
                except:
                    vg.miza_phf = None
                phf(self, vg.alegere_phf, vg.user_phf, vg.miza_phf)

            # Blackjack când o partidă e în curs
            if vg.user_blackjack == tags["display-name"] and cmd == "bj" and vg.on_bj:
                try:
                    temp = e.arguments[0].split()
                    vg.alegere_blackjack = temp[1]
                except:
                    pass
                blackjack(self, vg.alegere_blackjack, vg.user_blackjack, vg.miza_blackjack)

            # Blackjack când se începe o partidă
            elif cmd == "bj" and vg.user_blackjack is None and vg.on_bj:
                vg.user_blackjack = tags["display-name"]
                try:
                    temp = e.arguments[0].split()
                    vg.alegere_blackjack = temp[1]
                    vg.miza_blackjack = temp[2]
                except:
                    vg.miza_blackjack = None
                blackjack(self, vg.alegere_blackjack, vg.user_blackjack, vg.miza_blackjack)

            # Ruletă
            elif cmd == "ruleta" and tags["mod"] != "1" and vg.on_ruleta and tags["display-name"] != "ㄴㅇㅇㅇㅇㅇㄴ":
                jucator = tags["display-name"]
                if tags["subscriber"] == "1":
                    sub = 1
                else:
                    sub = 0
                ruleta(self, jucator, sub)

            # Grinch
            elif cmd == "grinch":
                user = tags["display-name"]
                if tags["subscriber"] == "1":
                    sub = 1
                else:
                    sub = 0
                grinch(self, user, sub)

            # Înscrie botul la Marbles
            elif cmd == "botplay":
                botplay(self)

            # Love
            elif cmd == "love":
                pers1 = tags["display-name"]
                try:
                    temp = e.arguments[0].split()
                    pers2 = ""
                    if len(temp) < 2:
                        pers2 = None
                    for i in range(1, len(temp)):
                        pers2 += temp[i]
                        if i != len(temp) - 1:
                            pers2 += " "
                except:
                    pers2 = None
                love(self, pers1, pers2)

            # Cuminte
            elif cmd == "cuminte":
                user = tags["display-name"]
                cuminte(self, user)

            # Oferă floare
            elif cmd == "flower":
               user = tags["display-name"]
               flower(self, user)

            # Video random
            elif cmd == "video":
                user = tags["display-name"]
                video_random(self, user)

            # Verifică câte puncte are userul
            elif cmd == "vons":
                user = tags["display-name"]
                try:
                    alt_user = e.arguments[0].split()
                    alt_user = alt_user[1]
                except:
                    alt_user = None
                puncte_user(self, user, alt_user)

            # Schimbă Vons în gamble points de la StreamElements
            elif cmd == "schimb":
                user = tags["display-name"]
                try:
                    puncte = e.arguments[0].split()
                    puncte = puncte[1]
                except:
                    puncte = None

                schimb_puncte(self, user, puncte)

            # Info Vons
            elif cmd == "ajutor":
                user = tags["display-name"]
                try:
                    alt_user = e.arguments[0].split()
                    alt_user = alt_user[1]
                except:
                    alt_user = None
                ajutor(self, user, alt_user)

            # Comenzi (help)
            elif cmd == 'comenzi':
                user = tags["display-name"]
                try:
                    alt_user = e.arguments[0].split()
                    alt_user = alt_user[1]
                except:
                    alt_user = None
                comenzi(self, user, alt_user)

        # Comenzi de MODS
        if e.arguments[0][:1] == '!' and (tags["mod"] == "1" or tags["display-name"].lower() == vg.owner):
            cmd = e.arguments[0].split(' ')[0][1:]
            mod = tags["display-name"]

            # Coinflip
            if cmd == 'coinflip':
                try:
                    nume = e.arguments[0].split()
                    nume = nume[1]
                except:
                    nume = None
                mods_coinflip(self, nume, mod)

            # Schimbă categoria
            elif cmd == "g":
                try:
                    categorie = e.arguments[0].split()
                    categorie = categorie[1]
                except:
                    categorie = None
                mods_schimba_categoria(self, categorie, mod)

            # Loto
            elif cmd == "loto":
                try:
                    reguli = e.arguments[0].split()
                    nr_min = reguli[1]
                    nr_max = reguli[2]
                    premiu = reguli[3]
                    vg.premiu_loto = int(premiu)
                except:
                    nr_min = None
                    nr_max = None
                    premiu = None
                mods_loto(self, nr_min, nr_max, premiu, mod)

            # Puncte de la redeem
            elif cmd == "puncte":
                try:
                    info = e.arguments[0].split()
                    user = info[1]
                    nr_puncte = int(info[2])
                except:
                    user = None
                    nr_puncte = None
                mods_puncte(self, mod, user, nr_puncte)

            # Top 10 flower
            elif cmd == "topflower":
                top_10_flower(self)

            # Minigame-uri on
            elif cmd == "on":
                try:
                    minijoc = e.arguments[0].split()
                    minijoc = minijoc[1]
                except:
                    minijoc = None
                on(self, mod, minijoc)

            # Minigame-uri off
            elif cmd == "off" and vg.user_blackjack is None and vg.user_phf is None:
                try:
                    minijoc = e.arguments[0].split()
                    minijoc = minijoc[1]
                except:
                    minijoc = None
                off(self, mod, minijoc)

            # Întrebări (comenzi)
            elif cmd in vg.intrebari:
                try:
                    nume = e.arguments[0].split()
                    nume = nume[1]
                except:
                    nume = None
                intrebari(self, cmd, nume)

        # Întrebări (răspunsuri automate)
        if "La ce facultate esti" in e.arguments[0] \
                or "la ce facultate esti" in e.arguments[0] \
                or "La ce facultate ai fost" in e.arguments[0] \
                or "la ce facultate ai fost" in e.arguments[0]:
            cmd = "facultate"
            nume = tags["display-name"]
            intrebari(self, cmd, nume)

        elif "Ce inaltime ai" in e.arguments[0] \
                or "ce inaltime ai" in e.arguments[0] \
                or "Cat esti de inalta" in e.arguments[0] \
                or "cat esti de inalta" in e.arguments[0]:
            cmd = "inaltime"
            nume = tags["display-name"]
            intrebari(self, cmd, nume)

        elif "Ce varsta ai" in e.arguments[0] \
                or "ce varsta ai" in e.arguments[0] \
                or "Cati ani ai" in e.arguments[0] \
                or "cati ani ai" in e.arguments[0]:
            cmd = "ani"
            nume = tags["display-name"]
            intrebari(self, cmd, nume)

        elif "cand te-ai apucat de stream" in e.arguments[0] \
                or "Cand te-ai apucat de stream" in e.arguments[0] \
                or "de cand te-ai apucat de stream" in e.arguments[0] \
                or "De cand te-ai apucat de stream" in e.arguments[0] \
                or "Cand ai inceput sa faci stream" in e.arguments[0] \
                or "cand ai inceput sa faci stream" in e.arguments[0] \
                or "De cand ai inceput sa faci stream" in e.arguments[0] \
                or "de cand ai inceput sa faci stream" in e.arguments[0] \
                or "de cat timp faci stream" in e.arguments[0] \
                or "De cat timp faci stream" in e.arguments[0]:
            cmd = "inceput"
            nume = tags["display-name"]
            intrebari(self, cmd, nume)

        elif "Ce zodie esti" in e.arguments[0] or "ce zodie esti" in e.arguments[0]:
            cmd = "zodie"
            nume = tags["display-name"]
            intrebari(self, cmd, nume)

        return