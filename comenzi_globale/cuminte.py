# Imports
import sys, random, os, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Cât de cuminte e userul
def cuminte(self, user):
    c = self.connection
    help_flag = True

    # Comanda când nu e cooldown
    if time() >= vg.timp_cuminte:

        # Acces la baza de date
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        procent = random.randint(0, 100)

        if procent >= 70:
            nr_puncte = 5000
        else:
            nr_puncte = -1000

        # Se extrag toți userii din baza de date dacă nu s-au extras deja
        if vg.data == []:
            for row in cursor.execute('''SELECT username FROM AVP'''):
                vg.data.append(row[0])

        # Userul este deja în baza de date
        if user in vg.data:
            # Acces la numărul de Vons al userului
            for row in cursor.execute('''SELECT puncte FROM AVP WHERE username = ?''', (user,)):
                temp = int(row[0]) + nr_puncte

                # Dacă s-au dat Vons cu - și userul ajunge la un număr negativ, se anulează partida
                if temp < 0:
                    conn.close()
                    help_flag = False
                    message = str(user) + ", nu mai încerca să abuzezi de acest bug deoarece nu mai funcționează WtfBruh"
                    c.privmsg(self.channel, message)

                break

            if help_flag:
                # Userul își primeste punctele
                cursor.execute('''UPDATE AVP SET puncte = ? WHERE username = ?''', (temp, user))

        # Userul nu e în baza de date și e introdus acum
        else:
            # Dacă s-au dat Vons cu -, se anulează partida
            if int(nr_puncte) < 0:
                conn.close()
                help_flag = False
                message = str(user) + ", nu mai încerca să abuzezi de acest bug deoarece nu mai funcționează WtfBruh"
                c.privmsg(self.channel, message)

            # Dacă nu s-au dat Vons cu +, userul primește numărul de Vons
            else:
                nr_puncte_temp = int(nr_puncte)

            if help_flag:
                # Userul își primește punctele
                cursor.execute('''INSERT INTO AVP (username, puncte) VALUES (?, ?)''', (user, nr_puncte_temp))
                temp = nr_puncte_temp
                vg.data.append(user)

        if help_flag:
            # Salvare și închidere baza de date
            conn.commit()
            conn.close()

            # Aici se schimbă cooldownul pentru comandă
            vg.timp_cuminte = time() + 60


            if procent >= 70:
                if nr_puncte == 1:
                    forma_puncte = " Von"
                elif nr_puncte == 0 or (nr_puncte % 100 > 0 and nr_puncte % 100 < 20):
                    forma_puncte = " Vons"
                else:
                    forma_puncte = " de Vons"

                message = str(user) + ", ai fost cuminte în proporție de " + str(procent) + "%. Ai primit " + f'{numbers.format_number(nr_puncte, locale="ro_RO")}' + forma_puncte + ". În prezent ai în total " + f'{numbers.format_number(temp, locale="ro_RO")}' + "."
            else:
                nr_puncte = nr_puncte * -1
                if nr_puncte == 1:
                    forma_puncte = " Von"
                elif nr_puncte == 0 or (nr_puncte % 100 > 0 and nr_puncte % 100 < 20):
                    forma_puncte = " Vons"
                else:
                    forma_puncte = " de Vons"
                
                message = str(user) + ", ai fost cuminte în proporție de " + str(procent) + "%. Ai pierdut " + f'{numbers.format_number(nr_puncte, locale="ro_RO")}' + forma_puncte + ". În prezent ai în total " + f'{numbers.format_number(temp, locale="ro_RO")}' + "."

            c.privmsg(self.channel, message)


    # Comanda când e cooldown
    elif time() < vg.timp_cuminte:
        timp_ramas = int(vg.timp_cuminte - time())
        completare = "următoarea încercare."

        c.privmsg(self.channel, cooldown(timp_ramas, user, completare))