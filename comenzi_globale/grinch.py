# Imports
import sys, random, os, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Subs fură de la plebs
def grinch(self, user, sub):
    c = self.connection

    # Cel puțin un pleb a scris deja în chat
    if len(vg.all_plebs) > 0:

        # Userul e sub
        if sub:

            # Comanda când nu e cooldown
            if time() >= vg.timp_grinch:

                # Acces la baza de date
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()

                nr_puncte = random.randint(1000, 2000)
                nr_pleb = random.randint(0, len(vg.all_plebs) - 1)
                pleb = vg.all_plebs[nr_pleb]
                nr_puncte_furate = 0

                # Se extrag toți userii din baza de date dacă nu s-au extras deja
                if vg.data == []:
                    for row in cursor.execute('''SELECT username FROM Vons'''):
                        vg.data.append(row[0])

                # Plebul este deja în baza de date
                if pleb in vg.data:
                    # Acces la numărul de Vons al plebului
                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (pleb,)):
                        if int(row[0]) < nr_puncte:
                            nr_puncte_furate = int(row[0])
                        else:
                            nr_puncte_furate = nr_puncte

                        temp = int(row[0]) - nr_puncte

                        # Dacă plebul ajunge la un număr negativ, se salvează că are 0 Vons
                        if temp < 0:
                            temp = 0

                        break

                    # Plebul își pierde punctele
                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''', (temp, pleb))

                # Plebul nu e în baza de date și e introdus acum
                else:

                    # Punctele plebului sunt setate la 0
                    cursor.execute('''INSERT INTO Vons (username, puncte) VALUES (?, ?)''', (pleb, 0))
                    nr_puncte_furate = 0
                    vg.data.append(pleb)

                # Dacă nu s-au furat puncte
                if nr_puncte_furate == 0:
                    message = str(user) + ", din păcate " + str(pleb) + " s-a apărat și nu ai reușit să-i furi Vons Sadge"

                # S-au furat puncte
                else:
                    # Userul este deja în baza de date
                    if user in vg.data:
                        # Acces la numărul de Vons al userului
                        for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                            temp = int(row[0]) + nr_puncte_furate
                            break

                        # Userul își primește punctele
                        cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''', (temp, user))

                    # Userul nu e în baza de date și e introdus acum
                    else:
                        # Userul își primește punctele
                        cursor.execute('''INSERT INTO Vons (username, puncte) VALUES (?, ?)''', (user, nr_puncte_furate))
                        vg.data.append(user)

                    if nr_puncte_furate == 1:
                        forma_puncte = " Von"
                    elif nr_puncte_furate == 0 or (nr_puncte_furate % 100 > 0 and nr_puncte_furate % 100 < 20):
                        forma_puncte = " Vons"
                    else:
                        forma_puncte = " de Vons"

                    message = str(user) + ", ai reușit să-i furi " + f'{numbers.format_number(nr_puncte_furate, locale="ro_RO")}' + forma_puncte + " lui " + str(pleb) + " WideHardo"

                # Salvare și închidere baza de date
                conn.commit()
                conn.close()

                # Aici se schimbă cooldownul pentru grinch, valoare exprimată în secunde
                vg.timp_grinch = time() + 180 # era 300 înainte

                c.privmsg(self.channel, message)

            # Comanda când e cooldown
            elif time() < vg.timp_grinch:
                timp_ramas = int(vg.timp_grinch - time())
                completare = "următorul jaf."

                c.privmsg(self.channel, cooldown(timp_ramas, user, completare))

        # Userul nu e sub
        else:
            message = str(user) + ", !grinch e o comandă doar pentru subs."
            c.privmsg(self.channel, message)

    else:
        message = str(user) + ", încă nu sunt plebs pe care-i poți fura Sadge"
        c.privmsg(self.channel, message)