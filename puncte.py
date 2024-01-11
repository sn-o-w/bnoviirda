# Imports
import variabile_globale as vg
import os, sqlite3, locale
from time import time
from babel import numbers

# Localizare bază de date
DATABASE = os.path.abspath("base.db")

# Puncte pentru persoanele din chat care au scris în chat în ultimele X minute
def puncte_chat(self, chat):
    c = self.connection

    # Acces la baza de date
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Se extrag toți userii din baza de date dacă nu s-au extras deja
    if vg.data == []:
        for row in cursor.execute('''SELECT username FROM Vons'''):
            vg.data.append(row[0])

    # Fiecare user din chat își primește punctele
    for user in chat:
        # Userul este deja în baza de date
        if user in vg.data:

            # Acces la numărul de Vons al userului
            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                # Aici se schimbă câte puncte să primească chatul
                temp = int(row[0]) + 100
                break

            # Userul își primește punctele
            cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''', (temp, user))

        # Userul nu e în baza de date și e introdus acum
        else:
            # Aici se schimbă câte puncte să primească chatul
            cursor.execute('''INSERT INTO Vons (username, puncte) VALUES (?, ?)''', (user, 100))
            vg.data.append(user)

    # Salvare și închidere baza de date
    conn.commit()
    conn.close()

    # Aici se schimbă cooldownul pentru puncte
    vg.chat = []
    vg.timp_puncte = time() + 600


# Arată câte puncte are un user
def puncte_user(self, user, alt_user):
    c = self.connection

    # Acces la baza de date
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Comandă simplă
    if alt_user is None or alt_user[0] != '@':
        temp = 0

        # Se extrag toți userii din baza de date dacă nu s-au extras deja
        if vg.data == []:
            for row in cursor.execute('''SELECT username FROM Vons'''):
                vg.data.append(row[0])

        # Userul este deja în baza de date
        if user in vg.data:
            # Acces la numărul de Vons al userului
            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                temp = row[0]
                break

        # Userul nu e în baza de date
        else:
            temp = 0

        if temp == 1:
            forma_temp = " Von"
        elif temp == 0 or (temp % 100 > 0 and temp % 100 < 20):
            forma_temp = " Vons"
        else:
            forma_temp = " de Vons"
            
        message = str(user) + ", ai în prezent " + f'{numbers.format_number(temp, locale="ro_RO")}' + forma_temp + "."
        c.privmsg(self.channel, message)

    # Comandă + mention
    else:
        # În baza de date userii sunt salvați fără @
        if alt_user[0] == '@':
            alt_user = alt_user[1:]

        temp = 0

        # Se extrag toți userii din baza de date dacă nu s-au extras deja
        if vg.data == []:
            for row in cursor.execute('''SELECT username FROM Vons'''):
                vg.data.append(row[0])

        # Userul este deja în baza de date
        if alt_user in vg.data:
            # Acces la numărul de Vons al userului
            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (alt_user,)):
                temp = row[0]
                break

        # Userul nu e în baza de date
        else:
            temp = 0

        if temp == 1:
            forma_temp = " Von"
        elif temp == 0 or (temp % 100 > 0 and temp % 100 < 20):
            forma_temp = " Vons"
        else:
            forma_temp = " de Vons"

        message = str(alt_user) + " are în prezent " + f'{numbers.format_number(temp, locale="ro_RO")}' + forma_temp + "."
        c.privmsg(self.channel, message)

    # Închidere baza de date
    conn.close()


# Vons de la redeem
def mods_puncte(self, mod, user, nr_puncte):
    c = self.connection

    # Comanda introdusă corect
    if user is not None and nr_puncte is not None and nr_puncte != 0:
        if user[0] == '@':
            user = user[1:]

        # Acces la baza de date
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Se extrag toți userii din baza de date dacă nu s-au extras deja
        if vg.data == []:
            for row in cursor.execute('''SELECT username FROM Vons'''):
                vg.data.append(row[0])

        # Când se dau Vons unui singur user
        if user != "all":

            # Userul este deja în baza de date
            if user in vg.data:
                # Acces la numărul de Vons al userului
                for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                    temp = int(row[0]) + nr_puncte

                    # Dacă s-au dat Vons cu - și userul ajunge la un număr negativ, se salvează că are 0 Vons
                    if temp < 0:
                        temp = 0

                    break

                # Userul își primește punctele
                cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''', (temp, user))

            # Userul nu e în baza de date și e introdus acum
            else:
                # Dacă s-au dat Vons cu -, se salvează că primește 0 Vons
                if int(nr_puncte) < 0:
                    nr_puncte_temp = 0

                # Dacă nu s-au dat Vons cu -, userul primește numărul de Vons
                else:
                    nr_puncte_temp = int(nr_puncte)

                # Userul își primește punctele
                cursor.execute('''INSERT INTO Vons (username, puncte) VALUES (?, ?)''', (user, nr_puncte_temp))
                temp = nr_puncte_temp
                vg.data.append(user)

            # Salvare și închidere baza de date
            conn.commit()
            conn.close()

            if nr_puncte == 1:
                forma_puncte = " Von"
            elif nr_puncte == 0 or (nr_puncte % 100 > 0 and nr_puncte % 100 < 20):
                forma_puncte = " Vons"
            else:
                forma_puncte = " de Vons"

            message = str(user) + ", ai primit " + f'{numbers.format_number(nr_puncte, locale="ro_RO")}' + forma_puncte + ". Acum ai în total " + f'{numbers.format_number(temp, locale="ro_RO")}' + "."
            c.privmsg(self.channel, message)

        # Când se dau Vons la tot chatul
        else:
            # Fiecare user din chat primește puncte
            for chatter in vg.all:

                # Userul este deja în baza de date
                if chatter in vg.data:
                    # Acces la numărul de Vons al userului
                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (chatter,)):
                        temp = int(row[0]) + int(nr_puncte)

                        # Dacă s-au dat Vons cu - și userul ajunge la un număr negativ, se salvează că are 0 Vons
                        if temp < 0:
                            temp = 0

                        break

                    # Userul își primește punctele
                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''', (temp, chatter))

                # Userul nu e în baza de date și e introdus acum
                else:
                    # Dacă s-au dat Vons cu -, se salvează că primește 0 Vons
                    if int(nr_puncte) < 0:
                        nr_puncte_temp = 0

                    # Dacă nu s-au dat Vons cu -, userul primește numărul de Vons
                    else:
                        nr_puncte_temp = int(nr_puncte)

                    # Userul își primește punctele
                    cursor.execute('''INSERT INTO Vons (username, puncte) VALUES (?, ?)''', (chatter, nr_puncte_temp))
                    vg.data.append(chatter)

            # Salvare și închidere baza de date
            conn.commit()
            conn.close()

            puncte_fara_minus = abs(nr_puncte)
            if puncte_fara_minus == 1:
                forma_puncte = " Von"
            elif puncte_fara_minus == 0 or (puncte_fara_minus % 100 > 0 and puncte_fara_minus % 100 < 20):
                forma_puncte = " Vons"
            else:
                forma_puncte = " de Vons"

            if int(nr_puncte) > 0:
                message = "Toată lumea a primit " + f'{numbers.format_number(nr_puncte, locale="ro_RO")}' + forma_puncte + ". EZY"
            else:
                message = "Toată lumea a primit " + f'{numbers.format_number(nr_puncte, locale="ro_RO")}' + forma_puncte + ". NotLikeThis"

            c.privmsg(self.channel, message)

    # Comandă introdusă greșit
    else:
        message = str(mod) + ", ai introdus comanda greșit. Trebuia: !puncte <user> <nr-întreg-de-puncte> 3Head Clap"
        c.privmsg(self.channel, message)


# Schimbă Vons în gamble points de la StreamElements
def schimb_puncte(self, user, puncte):
    c = self.connection

    # Verifică dacă comanda a fost introdusă corect
    if puncte != "all":
        try:
            puncte = int(puncte)
        except:
            puncte = None

    if puncte != "all" and puncte is not None:
        if puncte == 0:
            message = str(user) + ", nu poți schimba 0 Vons."
            c.privmsg(self.channel, message)
            return

        elif puncte < 0:
            message = str(user) + ", nu poți schimba un număr negativ de Vons."
            c.privmsg(self.channel, message)
            return

    if puncte is None:
        message = str(user) + ", ai introdus comanda greșit. Exemplu corect: !schimb 1000"
        c.privmsg(self.channel, message)

    # Comanda a fost introdusă corect
    else:
        # Acces la baza de date
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        temp = 0

        # Se extrag toți userii din baza de date dacă nu s-au extras deja
        if vg.data == []:
            for row in cursor.execute('''SELECT username FROM Vons'''):
                vg.data.append(row[0])

        # Userul este deja în baza de date
        if user in vg.data:
            # Acces la numărul de Vons al userului
            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                temp = row[0]
                break

        # Userul nu e în baza de date
        else:
            temp = 0

        # Userul vrea să-și schimbe toți Vons
        if puncte == "all":
            puncte = temp

            # Userul are 0 Vons
            if puncte == 0:
                message = str(user) + ", nu poți schimba Vons deoarece ai 0."
                c.privmsg(self.channel, message)

                return

        # Userul vrea să schimbe mai mulți Vons decât are
        if int(puncte) > int(temp):
            # Închidere baza de date
            conn.close()

            message = str(user) + ", nu ai destui Vons pentru a schimba " + f'{numbers.format_number(puncte, locale="ro_RO")}' + "."
            c.privmsg(self.channel, message)

        # Userul vrea să schimbe un număr de Vons pe care îl deține
        else:
            # Se retrag Vons
            cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',(temp - puncte, user))

            if puncte == 1:
                forma_puncte = " Von"
                forma_gamble_points = " gamble point"
            elif puncte == 0 or (puncte % 100 > 0 and puncte % 100 < 20):
                forma_puncte = " Vons"
                forma_gamble_points = " gamble points"
            else:
                forma_puncte = " de Vons"
                forma_gamble_points = " de gamble points"

            message = str(user) + ", ai reușit să schimbi " + f'{numbers.format_number(puncte, locale="ro_RO")}' + forma_puncte + " în " + f'{numbers.format_number(puncte, locale="ro_RO")}' + forma_gamble_points + " de la StreamElements."
            c.privmsg(self.channel, message)

            message = "!addpoints " + str(user) + " " + str(puncte)
            c.privmsg(self.channel, message)

            # Salvare și închidere baza de date
            conn.commit()
            conn.close()

# Top 10 Vons
def top_10_vons(self):
    c = self.connection

    # Acces la baza de date
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    top_10 = []
    for row in cursor.execute('''SELECT * FROM Vons ORDER BY puncte DESC LIMIT 10'''):
        top_10.append(row)

    message = '; '.join([f'{i + 1}. {top_10[i][0]} ({numbers.format_number(top_10[i][1], locale="ro_RO")})' for i in range(len(top_10))])

    c.privmsg(self.channel, message)