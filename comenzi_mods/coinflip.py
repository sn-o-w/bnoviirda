# Imports
import sqlite3, random, os, sys
sys.path.append("..")
from timeout import timeout

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Coinflip
def mods_coinflip(self, nume, mod):
    c = self.connection

    # Comandă + mention
    if nume is not None:
        num = random.randint(1, 10)

        # VIP
        if num % 2 == 0:
            message = "Se va decide soarta lui " + str(nume) +". A picat " + str(num) +", deci VIP EZY Clap"
            c.privmsg(self.channel, message)

            # Acces la baza de date
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Ultimul VIP
            for row in cursor.execute('''SELECT username FROM VIPS ORDER BY id DESC LIMIT 1'''):
                last_vip = row[0]
                message = "@adriivonb, " + str(last_vip) + " a fost ultimul VIP."
                c.privmsg(self.channel, message)

            # Cel mai recent VIP este salvat în baza de date
            cursor.execute('''INSERT INTO VIPS (username) VALUES (?)''', (nume,))

            # Salvare și închidere bază de date
            conn.commit()
            conn.close()

        # Timeout
        else:
            message = "Se va decide soarta lui " + str(nume) + ". A picat " + str(num) + ", deci timeout MODS"
            c.privmsg(self.channel, message)

            timeout(nume, 86400, "Ai pierdut la coinflip")

    # Comandă fără mention
    else:
        message = str(mod) + ", trebuie să dai și mention userului care vrea coinflipul."
        c.privmsg(self.channel, message)