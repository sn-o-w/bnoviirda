# Imports
import os, sys, random, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Tradu alegerile scrise fără diacritice
def alegere_cu_fara_diacritice(alegere):
    variatii = {
        "piatra": "piatră",
        "hartie": "hârtie",
        "foarfeca": "foarfecă",
    }

    return variatii.get(alegere, alegere)

# Jocul de piatră, hârtie, foarfecă
def phf(self, alegere, user, miza):
    c = self.connection

    alegeri = ["piatră", "hârtie", "foarfecă"]

    # Comanda când nu e cooldown
    if time() >= vg.timp_phf:
        # Verifică dacă comanda a fost introdusă corect
        if miza != "all":
            try:
                miza = int(miza)
                vg.miza_phf = miza
            except:
                miza = None

        if miza != "all" and miza is not None:
            if miza == 0:
                message = str(user) + ", nu poți miza 0 Vons."
                c.privmsg(self.channel, message)
                vg.user_phf = None
                vg.alegere_phf = None
                vg.miza_phf = None
                return

            elif miza < 0:
                message = str(user) + ", nu poți miza nu număr negativ de Vons."
                c.privmsg(self.channel, message)
                vg.user_phf = None
                vg.alegere_phf = None
                vg.miza_phf = None
                return

        if alegere_cu_fara_diacritice(alegere) is None or miza is None:
            message = str(user) + ", ai introdus comanda greșit. Exemplu corect: !joc piatră 1000"
            vg.user_phf = None
            vg.alegere_phf = None
            vg.miza_phf = None
            c.privmsg(self.channel, message)

        elif alegere_cu_fara_diacritice(alegere) not in alegeri:
            message = str(user) + ", singurele alegeri posibile sunt: piatră, hârtie sau foarfecă."
            vg.user_phf = None
            vg.alegere_phf = None
            vg.miza_phf = None
            c.privmsg(self.channel, message)

        # Comanda a fost introdusă corect
        else:
            alegere = alegere_cu_fara_diacritice(alegere.lower())

            # Acces la baza de date
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Verifică câți Vons are userul
            if vg.flag_puncte_phf:
                temp = 0
                if vg.data == []:
                    for row in cursor.execute('''SELECT username FROM Vons'''):
                        vg.data.append(row[0])

                if user in vg.data:
                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                        temp = row[0]
                        break
                else:
                    temp = 0

                vg.puncte_temp_phf = temp

                if miza == "all":
                    miza = int(vg.puncte_temp_phf)
                    vg.miza_phf = miza

                    if vg.miza_phf == 0:
                        # Închidere baza de date
                        conn.close()

                        message = str(user) + ", nu poți miza deoarece ai 0 Vons."
                        c.privmsg(self.channel, message)

                        # Jocul se reinițializează
                        vg.user_phf = None
                        vg.alegere_phf = None
                        vg.miza_phf = None
                        vg.flag_puncte_phf = True
                        vg.puncte_temp_phf = None

                        return

            # Userul vrea să mizeze mai mulți Vons decât are
            if int(miza) > int(vg.puncte_temp_phf):
                # Închidere baza de date
                conn.close()

                message = str(user) + ", nu ai destui Vons pentru a miza " + f'{numbers.format_number(miza, locale="ro_RO")}' + "."
                c.privmsg(self.channel, message)

                # Jocul se reinițializează
                vg.user_phf = None
                vg.alegere_phf = None
                vg.miza_phf = None
                vg.flag_puncte_phf = True
                vg.puncte_temp_phf = None

            # Miza este acceptată
            else:
                # Miza este pariată
                if vg.flag_puncte_phf:
                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                   (vg.puncte_temp_phf - vg.miza_phf, user))

                    # Salvare baza de date
                    conn.commit()

                    vg.flag_puncte_phf = False

                # Alegerea botului
                alegere_bot = random.randint(0, 2)
                alegere_bot = alegeri[alegere_bot]

                # Remiză între user și bot
                if alegere == alegere_bot:
                    message = str(user) + ", tu ai ales " + str(alegere) + ", iar botul a ales tot " + str(alegere_bot) + ". Rejoacă rapid partida până nu o pierzi prin descalificare."
                    c.privmsg(self.channel, message)

                    vg.pedeapsa_phf = time() + 30

                    # Închidere baza de date
                    conn.close()

                # Userul a câștigat
                elif (alegere == "piatră" and alegere_bot == "foarfecă") or (alegere == "hârtie" and alegere_bot == "piatră") or (alegere == "foarfecă" and alegere_bot == "hârtie"):

                    if vg.miza_phf == 1:
                        forma_miza = " Von"
                    elif vg.miza_phf == 0 or (vg.miza_phf % 100 > 0 and vg.miza_phf % 100 < 20):
                        forma_miza = " Vons"
                    else:
                        forma_miza = " de Vons"

                    message = str(user) + ", tu ai ales " + str(alegere) + ", iar botul a ales " + str(alegere_bot) + ". Bravo, ți-ai dublat miza de " + f'{numbers.format_number(vg.miza_phf, locale="ro_RO")}' + forma_miza + "."
                    c.privmsg(self.channel, message)

                    # Acces la numărul de Vons al userului
                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                        vg.puncte_temp_phf = row[0]
                        break

                    # Userul își primește câștigul
                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                   (vg.puncte_temp_phf + vg.miza_phf * 2, user))

                    # Salvare și închidere baza de date
                    conn.commit()
                    conn.close()

                    # Aici se schimbă cooldownul pentru phf și se reinițializează jocul
                    vg.timp_phf = time() + 300
                    vg.pedeapsa_phf = time()
                    vg.user_phf = None
                    vg.alegere_phf = None
                    vg.miza_phf = None
                    vg.flag_puncte_phf = True
                    vg.puncte_temp_phf = None

                # Userul a pierdut
                elif (alegere_bot == "piatră" and alegere == "foarfecă") or (alegere_bot == "hârtie" and alegere == "piatră") or (alegere_bot == "foarfecă" and alegere == "hârtie"):

                    if vg.miza_phf == 1:
                        forma_miza = " Von"
                    elif vg.miza_phf == 0 or (vg.miza_phf % 100 > 0 and vg.miza_phf % 100 < 20):
                        forma_miza = " Vons"
                    else:
                        forma_miza = " de Vons"

                    message = str(user) + ", tu ai ales " + str(alegere) + ", iar botul a ales " + str(alegere_bot) + ". Ți-ai pierdut miza de " + f'{numbers.format_number(vg.miza_phf, locale="ro_RO")}' + forma_miza + "."
                    c.privmsg(self.channel, message)

                    # Închidere baza de date
                    conn.close()

                    # Aici se schimbă cooldownul pentru phf și se reinițializează jocul
                    vg.timp_phf = time() + 300
                    vg.pedeapsa_phf = time()
                    vg.user_phf = None
                    vg.alegere_phf = None
                    vg.miza_phf = None
                    vg.flag_puncte_phf = True
                    vg.puncte_temp_phf = None

    # Comanda când e cooldown
    elif time() < vg.timp_phf:
        timp_ramas = int(vg.timp_phf - time())
        completare = "următoarea partidă de piatră, hârtie, foarfecă."

        vg.user_phf = None
        vg.alegere_phf = None
        vg.miza_phf = None
        c.privmsg(self.channel, cooldown(timp_ramas, user, completare))


# Penalizare la piatră, hârtie, foarfecă
def penalizare_phf(self, user, miza):
    c = self.connection

    message = str(user) + ", ai așteptat prea mult înainte să rejoci partida anterioară," + " ceea ce înseamnă că ți-ai pierdut miza de " + f'{numbers.format_number(miza, locale="ro_RO")}' + " Vons prin descalificare."
    c.privmsg(self.channel, message)

    # Aici se schimbă cooldownul pentru phf și se reinițializează jocul
    vg.timp_phf = time() + 300
    vg.pedeapsa_phf = time()
    vg.user_phf = None
    vg.alegere_phf = None
    vg.miza_phf = None
    vg.flag_puncte_phf = True
    vg.puncte_temp_phf = None