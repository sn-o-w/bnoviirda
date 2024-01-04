# Imports
import sys, random, os, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Oferă floricică
def flower(self, user):
    c = self.connection

    # Comanda când nu e cooldown
    if time() >= vg.timp_flower and len(vg.all) > 1:

        # Acces la baza de date
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Se extrag toți userii din baza de date, care au primit deja cel puțin o floricică, dacă nu s-au extras deja
        if vg.all_flower == []:
            for row in cursor.execute('''SELECT username FROM Flowers'''):
                vg.all_flower.append(row[0])

        # Numărul de flori
        nr_flori = random.randint(1, 3)

        # Destinatar
        destinatar = None
        while (destinatar == None or destinatar == user):
            nr_destinatar = random.randint(0, len(vg.all) - 1)
            destinatar = vg.all[nr_destinatar]

        # Destinatarul a primit deja cel puțin o floricică
        if destinatar in vg.all_flower:
            # Acces la numărul de flori al destinatarului
            cursor.execute('''SELECT flori FROM Flowers WHERE username = ?''', (destinatar,))
            temp = cursor.fetchone()[0] + nr_flori

            # Destinatarul își primește floricelele
            cursor.execute('''UPDATE Flowers SET flori = ? WHERE username = ?''', (temp, destinatar))

        # Destinatarul nu a primit floricele până acum
        else:
            # Destinatarul își primește floricelele
            cursor.execute('''INSERT INTO Flowers (username, flori) VALUES (?, ?)''', (destinatar, nr_flori))
            vg.all_flower.append(destinatar)

        # Salvare și închidere baza de date
        conn.commit()
        conn.close()

        if nr_flori == 1:
            forma_flori = " floricică"
        elif nr_flori == 0 or (nr_flori % 100 > 0 and nr_flori % 100 < 20):
            forma_flori = " floricele"
        else:
            forma_flori = " de floricele"

        message = str(destinatar) + " a primit " + f'{numbers.format_number(nr_flori, locale="ro_RO")}' + forma_flori + " de la " + str(user) + " DankFlower"
        c.privmsg(self.channel, message)

        # Aici se schimbă cooldownul pentru comandă
        vg.timp_flower = time() + 120

    # Comanda când e cooldown
    elif time() < vg.timp_flower:
        timp_ramas = int(vg.timp_flower - time())
        completare = "următoarea floricică."

        c.privmsg(self.channel, cooldown(timp_ramas, user, completare))

    # Insuficienți useri pe chat cărora să le dai floricele
    else:
        message = str(user) + ", nu există suficienți useri pe chat cărora să le dai floricele Sadge"
        c.privmsg(self.channel, message)

# Top 10 flower
def top_10_flower(self):
    c = self.connection

    # Acces la baza de date
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    top_10 = []
    for row in cursor.execute('''SELECT * FROM Flowers ORDER BY flori DESC LIMIT 10'''):
        top_10.append(row)

    #message = str(i+1) + ". " + str(top_10[i][0]) + " cu " + str(top_10[i][1]) + " DankFlower"
    message = '; '.join([f'{i + 1}. {top_10[i][0]} ({top_10[i][1]})' for i in range(len(top_10))])

    c.privmsg(self.channel, message)