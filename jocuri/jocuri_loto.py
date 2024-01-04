# Imports
import os, sys, random, sqlite3
sys.path.append("..")
import variabile_globale as vg
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Loto
def mods_loto(self, nr_min, nr_max, premiu, mod):
    c = self.connection

    # Comanda introdusă corect
    if nr_min is not None and nr_max is not None and premiu is not None:
        # Nu se poate acorda un număr negativ de Vons drept premiu
        if int(premiu) < 0:
            message = str(mod) + ", nu poți acorda un număr negativ de Vons drept premiu."
            c.privmsg(self.channel, message)
            return

        # Nu se poate acorda 0 Vons drept premiu
        elif int(premiu) == 0:
            message = str(mod) + ", nu poți acorda 0 Vons drept premiu."
            c.privmsg(self.channel, message)
            return

        nr_1 = int(nr_min)
        nr_2 = int(nr_max)
        premiu = int(premiu)

        # Se alege numărul câștigător
        vg.numar_loto = random.randint(nr_1, nr_2)

        if premiu == 1:
            forma_premiu = " Von"
        elif premiu == 0 or (premiu % 100 > 0 and premiu % 100 < 20):
            forma_premiu = " Vons"
        else:
            forma_premiu = " de Vons"

        message = "Runda de loto a început! Cine ghicește numărul între " + str(nr_min) + " și " + str(
            nr_max) + " va primi " + f'{numbers.format_number(premiu, locale="ro_RO")}' + forma_premiu + "!"
        c.privmsg(self.channel, message)

    # Comandă introdusă greșit
    else:
        message = str(mod) + ", ai introdus comanda greșit. Trebuia: !loto <nr_min> <nr_max> <premiu> 3Head Clap"
        c.privmsg(self.channel, message)


# Când cineva ghicește numărul câștigător
def loto_castigat(self, jucator):
    c = self.connection

    if vg.premiu_loto == 1:
        forma_premiu = " Von"
    elif vg.premiu_loto == 0 or (vg.premiu_loto % 100 > 0 and vg.premiu_loto % 100 < 20):
        forma_premiu = " Vons"
    else:
        forma_premiu = " de Vons"

    message = str(jucator) + " a ghicit numărul " + str(vg.numar_loto) + " și va primi " + f'{numbers.format_number(vg.premiu_loto, locale="ro_RO")}' + forma_premiu + "!"
    c.privmsg(self.channel, message)

    # Acces la baza de date
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Se extrag toți userii din baza de date dacă nu s-au extras deja
    if vg.data == []:
        for row in cursor.execute('''SELECT username FROM AVP'''):
            vg.data.append(row[0])

    # Se verifică dacă câștigătorul e în baza de date
    # Câștigătorul e deja în baza de date
    if jucator in vg.data:
        # Acces la numărul de Vons al câștigătorulului
        for row in cursor.execute('''SELECT puncte FROM AVP WHERE username = ?''',
                                  (jucator,)):
            temp = int(row[0]) + vg.premiu_loto
            break

        # Câștigătorul își primește premiul
        cursor.execute('''UPDATE AVP SET puncte = ? WHERE username = ?''',
                       (temp, jucator))

    # Câștigătorul nu e în baza de date și e introdus acum
    else:
        # Câștigătorul își primește premiul
        cursor.execute('''INSERT INTO AVP (username, puncte) VALUES (?, ?)''',
                       (jucator, int(vg.premiu_lot)))
        vg.data.append(jucator)

    # Salvare și închidere baza de date
    conn.commit()
    conn.close()

    vg.numar_loto = None
    vg.premiu_loto = None
