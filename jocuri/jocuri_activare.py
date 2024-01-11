# Imports
import sys
sys.path.append("..")
import variabile_globale as vg
from time import time

# Blackjack on automat
def on_auto(self):
    c = self.connection

    vg.timp_blackjack = time()
    vg.on_bj = True

    message = "@chat, s-a pornit blackjackul."
    c.privmsg(self.channel, message)

# Blackjack off automat
def off_auto(self):
    c = self.connection

    vg.on_bj = False
    vg.bj_off_automat = False

    message = "@chat, s-a oprit blackjackul."
    c.privmsg(self.channel, message)

# Minigame-uri on
def on(self, mod, minigame):
    c = self.connection

    # Comandă fără minigame
    if minigame is None:
        message = str(mod) + ", nu ai ales ce minigame vrei să pornești. Ex.: !on bj"

    # Comandă + minigame
    else:
        # Blackjack când e off
        if minigame == "bj" and not vg.on_bj:
            vg.on_bj = True
            vg.timp_blackjack = time()
            message = str(mod) + ", ai pornit blackjackul."

        # Blackjack cand e on
        elif minigame == "bj":
            message = str(mod) + ", blackjackul este deja pornit."

        # Piatră, hârtie, foarfecă când e off
        elif minigame == "phf" and not vg.on_phf:
            vg.on_phf = True
            vg.timp_phf = time()
            message = str(mod) + ", ai pornit jocul de piatră, hârtie, foarfecă."

        # Piatră, hârtie, foarfecă când e on
        elif minigame == "phf":
            message = str(mod) + ", jocul de piatră, hârtie, foarfecă este deja pornit."

        # Ruleta când e off
        elif minigame == "ruleta" and not vg.on_ruleta:
            vg.on_ruleta = True
            vg.timp_ruleta = time()
            message = str(mod) + ", ai pornit ruleta."

        # Ruleta când e on
        elif minigame == "ruleta":
            message = str(mod) + ", ruleta este deja pornită."

        # Minigame ce nu există
        else:
            message = str(mod) + ", ai vrut să pornești un minigame pe care nu-l avem sau ai greșit comanda."

    c.privmsg(self.channel, message)

# Minigame-uri off
def off(self, mod, minigame):
    c = self.connection

    # Comandă fără minigame
    if minigame is None:
        message = str(mod) + ", nu ai ales ce minigame vrei să oprești. Ex.: !off bj"

    # Comandă + minigame
    else:
        # Blackjack când e on
        if minigame == "bj" and vg.on_bj:
            vg.on_bj = False
            message = str(mod) + ", ai oprit blackjackul."

        # Blackjack când e off
        elif minigame == "bj":
            message = str(mod) + ", blackjackul este deja oprit."

        # Piatră, hârtie, foarfecă când e on
        elif minigame == "phf" and vg.on_phf:
            vg.on_phf = False
            message = str(mod) + ", ai oprit jocul de piatră, hârtie, foarfecă."

        # Piatră, hârtie, foarfecă când e off
        elif minigame == "phf":
            message = str(mod) + ", jocul de piatră, hârtie, foarfecă este deja oprit."

        # Ruleta când e on
        elif minigame == "ruleta" and vg.on_ruleta:
            vg.on_ruleta = False
            message = str(mod) + ", ai oprit ruleta."

        # Ruleta când e off
        elif minigame == "ruleta":
            message = str(mod) + ", ruleta este deja oprită."

        # Minigame ce nu există
        else:
            message = str(mod) + ", ai vrut să oprești un minigame pe care nu-l avem sau ai greșit comanda."

    c.privmsg(self.channel, message)