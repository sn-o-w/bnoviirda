# Imports
import sys
sys.path.append("..")
import variabile_globale as vg
from time import time

link_vons = "https://i.epvpimg.com/divaeab.png"
link_comenzi = "https://i.epvpimg.com/VYBzbab.png"

# Comenzi (help)
def comenzi(self, user, alt_user):
    c = self.connection

    # Comandă simplă
    if alt_user is None or alt_user[0] != '@':
        message = str(user) + ", aici ai toate comenzile botului: " + link_comenzi

    # Comandă + mention
    else:
        message = str(alt_user) + ", aici ai toate comenzile botului: " + link_comenzi

    c.privmsg(self.channel, message)

# Ajutor Vons
def ajutor(self, user, alt_user):
    c = self.connection

    if user is not None:
        # Comandă simplă
        if alt_user is None or alt_user[0] != '@':
            message = str(user) + ", aici ai informații despre Vons: " + link_vons

        # Comandă + mention @chat
        elif alt_user == "@chat":
            message = str(alt_user) + ", aici aveți informații despre Vons: " + link_vons

        # Comandă + mention
        else:
            message = str(alt_user) + ", aici ai informații despre Vons: " + link_vons

    # Cooldown pentru comanda dată automat
    else:
        message = str(alt_user) + ", aici aveți informații despre Vons: " + link_vons
        message2 = str(alt_user) + ", aici aveți toate comenzile botului: " + link_comenzi
        c.privmsg(self.channel, message2)

        vg.timp_ajutor = time() + 1800

    c.privmsg(self.channel, message)

# Înscrie botul la Marbles
def botplay(self):
    c = self.connection

    message = "!play"
    c.privmsg(self.channel, message)

# Mesaj pentru userii noi din chat
def new_user(self, user):
    c = self.connection

    message = str(user) + ", bun-venit la noi în chat! PogU"
    c.privmsg(self.channel, message)