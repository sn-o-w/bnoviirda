# Imports
import os, sys, random, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from timeout import timeout

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Joc de ruletă
def ruleta(self, jucator, sub):
    c = self.connection

    # Userul e sub
    if sub == 1:

        # Comanda când nu e cooldown
        if time() >= vg.timp_ruleta:
            num = random.randint(1, 10)

            # Userul a câștigat
            if num % 2 == 0:
                # Acces la baza de date
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()

                if vg.premiu_ruleta == 1000:
                    message = str(jucator) + " își încearcă norocul la ruletă. " + str(jucator) +\
                              " a supraviețuit și va primi " + str(vg.premiu_ruleta//1000) + "k Vons. Premiul rămâne de 1k."

                else:
                    message = str(jucator) + " își încearcă norocul la ruletă. " + str(jucator) +\
                              " a supraviețuit și va primi " + str(vg.premiu_ruleta // 1000) + \
                              "k Vons. Premiul s-a resetat acum la 1k."

                c.privmsg(self.channel, message)

                # Se extrag toți userii din baza de date dacă nu s-au extras deja
                if vg.data == []:
                    for row in cursor.execute('''SELECT username FROM AVP'''):
                        vg.data.append(row[0])

                # Se verifică dacă câștigătorul e în baza de date
                # Câștigătorul e deja în baza de date
                if jucator in vg.data:
                    # Acces la numărul de Vons al câștigătorului
                    for row in cursor.execute('''SELECT puncte FROM AVP WHERE username = ?''', (jucator,)):
                        temp = int(row[0]) + vg.premiu_ruleta
                        break

                    # Câștigătorul își primește premiul
                    cursor.execute('''UPDATE AVP SET puncte = ? WHERE username = ?''', (temp, jucator))

                # Câștigătorul nu e în baza de date și e introdus acum
                else:
                    # Câștigătorul își primește premiul
                    cursor.execute('''INSERT INTO AVP (username, puncte) VALUES (?, ?)''', (jucator, int(vg.premiu_ruleta)))
                    vg.data.append(jucator)

                # Premiul se resetează la valoarea inițială
                vg.premiu_ruleta = 1000

                # Salvare și închidere bază de date
                conn.commit()
                conn.close()

            # Userul a pierdut
            else:
                vg.premiu_ruleta += 1000
                message = str(jucator) + " își încearcă norocul la ruletă. " + str(jucator) + \
                          " nu a supraviețuit, dar va reveni printre noi peste 90 de secunde. Premiul a crescut la " \
                          + str(vg.premiu_ruleta//1000) +"k Vons."
                c.privmsg(self.channel, message)

                timeout(jucator, 90, "Ai pierdut la ruletă.")

            # Aici se schimbă cooldownul pentru ruletă
            vg.timp_ruleta = time() + 180

        # Comanda când e cooldown
        elif time() < vg.timp_ruleta:
            timp_ramas = int(vg.timp_ruleta - time())
            completare = "următoarea partidă de ruletă."

            c.privmsg(self.channel, cooldown(timp_ramas, jucator, completare))

    # Userul nu e sub
    else:
        message = str(jucator) + ", !ruleta e o comandă doar pentru subs."
        c.privmsg(self.channel, message)