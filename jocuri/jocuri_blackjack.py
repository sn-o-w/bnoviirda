# Imports
import os, sys, random, sqlite3
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown
from babel import numbers

# Localizare baza de date
DATABASE = os.path.abspath("base.db")

# Jocul de blackjack
def blackjack(self, alegere, user, miza):
    c = self.connection

    # Comanda când nu e cooldown
    if time() >= vg.timp_blackjack:
        alegeri = ["start", "+", "1", "11", "stop"]
        carti = ["x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        # Verifică dacă comanda a fost introdusă corect
        if miza != "all":
            try:
                miza = int(miza)
                vg.miza_blackjack = miza
            except:
                miza = None

        if miza != "all" and miza is not None:
            if miza == 0:
                message = str(user) + ", nu poți miza 0 Vons."
                c.privmsg(self.channel, message)
                vg.user_blackjack = None
                vg.alegere_blackjack = None
                vg.miza_blackjack = None
                return

            elif miza < 0:
                message = str(user) + ", nu poți miza un număr negativ de Vons."
                c.privmsg(self.channel, message)
                vg.user_blackjack = None
                vg.alegere_blackjack = None
                vg.miza_blackjack = None
                return

        if alegere is None or miza is None:
            message = str(user) + ", nu ai introdus comanda corect. Exemplu corect: !bj start 1000"
            vg.user_blackjack = None
            vg.alegere_blackjack = None
            c.privmsg(self.channel, message)

        elif alegere not in alegeri:
            message = str(user) + ", singurele alegeri posibile sunt: start, +, 1, 11 sau stop."
            if not vg.flag_start_blackjack:
                vg.user_blackjack = None
            vg.alegere_blackjack = None
            c.privmsg(self.channel, message)

        # Comanda e introdusă corect
        else:
            alegere = alegere.lower()

            # Acces la baza de date
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Verifică câți Vons are userul
            if vg.flag_puncte_blackjack:
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

                vg.puncte_temp_blackjack = temp

                if miza == "all":
                    miza = int(vg.puncte_temp_blackjack)
                    vg.miza_blackjack = miza

                    if vg.miza_blackjack == 0:
                        # Închidere baza de date
                        conn.close()

                        message = str(user) + ", nu poți miza deoarece ai 0 Vons."
                        c.privmsg(self.channel, message)

                        # Jocul se reinițializează
                        vg.user_blackjack = None
                        vg.alegere_blackjack = None
                        vg.miza_blackjack = None
                        vg.flag_puncte_blackjack = True
                        vg.puncte_temp_blackjack = None

                        return

            # Userul vrea să mizeze mai mulți Vons decât are
            if int(miza) > int(vg.puncte_temp_blackjack):
                # Închidere baza de date
                conn.close()

                message = str(user) + ", nu ai destui Vons pentru a miza " + \
                        f'{numbers.format_number(miza, locale="ro_RO")}' + "."
                c.privmsg(self.channel, message)

                # Jocul se reinițializează
                vg.user_blackjack = None
                vg.alegere_blackjack = None
                vg.miza_blackjack = None
                vg.flag_puncte_blackjack = True
                vg.puncte_temp_blackjack = None

            # Miza este acceptată
            else:
                # Miza este pariată
                if vg.flag_puncte_blackjack:
                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                   (vg.puncte_temp_blackjack - vg.miza_blackjack, user))

                    # Salvare baza de date
                    conn.commit()

                    vg.flag_puncte_blackjack = False

                # Carte 1
                nr_carte_1 = random.randint(2, 14)
                carte_1 = carti[nr_carte_1]

                # Începutul partidei
                if alegere == "start" and not vg.flag_start_blackjack:
                    # Carte 1 bot
                    nr_carte_1_bot = random.randint(2, 13)
                    carte_1_bot = carti[nr_carte_1_bot]
                    vg.carti_blackjack_bot.append(carte_1_bot)

                    if nr_carte_1_bot >= 2 and nr_carte_1_bot <= 10:
                        vg.total_blackjack_bot += nr_carte_1_bot

                    elif nr_carte_1_bot > 10 and nr_carte_1_bot <= 13:
                        vg.total_blackjack_bot += 10

                    # Carte 2
                    nr_carte_2 = random.randint(2, 13)
                    carte_2 = carti[nr_carte_2]

                    # Analiză a cărților + calculare total
                    if carte_1 == "A":
                        if nr_carte_2 >= 2 and nr_carte_2 <= 10:
                            vg.total_blackjack += nr_carte_2

                        elif nr_carte_2 > 10 and nr_carte_2 <= 13:
                            vg.total_blackjack += 10

                        message = str(user) + ", ai tras un " + carte_2 + " și un " + carte_1 + \
                                  ". Scrie rapid „!bj 1” pentru as = 1 sau „!bj 11” pentru as = 11" + \
                                  ". Prima carte a botului e " + str(carte_1_bot) + "."

                        vg.flag_as_blackjack = True

                    else:
                        if nr_carte_1 >= 2 and nr_carte_1 <= 10:
                            vg.total_blackjack += nr_carte_1

                        elif nr_carte_1 > 10 and nr_carte_1 <= 13:
                            vg.total_blackjack += 10

                        if nr_carte_2 >= 2 and nr_carte_2 <= 10:
                            vg.total_blackjack += nr_carte_2

                        elif nr_carte_2 > 10 and nr_carte_2 <= 13:
                            vg.total_blackjack += 10

                        message = str(user) + ", ai tras un " + carte_2 + " și un " + carte_1 + \
                                  ", ai în total " + str(vg.total_blackjack) + \
                                  ". Scrie rapid „!bj +” pentru a mai trage o carte sau „!bj stop” pentru a te opri" + \
                                  ". Prima carte a botului e " + str(carte_1_bot) + "."

                    c.privmsg(self.channel, message)

                    # Aici se pune timpul de așteptare pentru pedeapsă
                    vg.pedeapsa_blackjack = time() + 40
                    vg.flag_start_blackjack = True

                    # Închidere baza de date
                    conn.close()

                # Când userul a tras un as
                elif (alegere == "1" or alegere == "11") and vg.flag_as_blackjack and vg.flag_start_blackjack:
                    # Total + 11 dacă a ales as = 11 sau total + 1 dacă a ales as = 1
                    vg.total_blackjack += int(alegere)

                    # Userul nu are 21
                    if vg.total_blackjack != 21:
                        message = str(user) + ", ai ales as = " + alegere + ", ai în total " + str(vg.total_blackjack) + \
                                  ". Scrie rapid „!bj +” pentru a mai trage o carte sau „!bj stop” pentru a te opri."

                        # Aici se pune timpul de așteptare pentru pedeapsă
                        vg.pedeapsa_blackjack = time() + 40

                    # Userul are 21
                    else:
                        # Cărți + total bot
                        carti_total_bot(carti)

                        # Botul nu a obținut 21
                        if vg.total_blackjack_bot != 21:
                            if vg.miza_blackjack == 1:
                                forma_miza = " Von"
                            elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                forma_miza = " Vons"
                            else:
                                forma_miza = " de Vons"
                          
                            message = str(user) + ", ai tras un " + carte_1 + \
                                      ", ai în total " + str(vg.total_blackjack) + \
                                      ". Ai câștigat pentru că botul a obținut " + str(vg.total_blackjack_bot) + \
                                      ". Ți-ai dublat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                      ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                            # Acces la numărul de Vons al userului
                            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                vg.puncte_temp_blackjack = row[0]
                                break

                            # Userul își primește câștigul
                            cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                           (vg.puncte_temp_blackjack + vg.miza_blackjack * 2, user))

                            # Salvare baza de date
                            conn.commit()

                        # Botul a obținut și el 21
                        else:
                            if vg.miza_blackjack == 1:
                                forma_miza = " Von"
                            elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                forma_miza = " Vons"
                            else:
                                forma_miza = " de Vons"

                            message = str(user) + ", ai tras un " + carte_1 + \
                                      ", ai în total " + str(vg.total_blackjack) + \
                                      ". S-a terminat egal deoarece și botul a obținut " + str(vg.total_blackjack_bot) + \
                                      ". Ti-ai recuperat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                      ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                            # Acces la numărul de Vons al userului
                            for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                vg.puncte_temp_blackjack = row[0]
                                break

                            # Userul își reprimește miza
                            cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                           (vg.puncte_temp_blackjack + vg.miza_blackjack, user))

                            # Salvare baza de date
                            conn.commit()

                        # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
                        reinitializare()

                    c.privmsg(self.channel, message)
                    vg.flag_as_blackjack = False

                    # Închidere baza de date
                    conn.close()

                # Userul mai trage o carte
                elif alegere == "+" and vg.flag_start_blackjack and not vg.flag_as_blackjack:
                    # Analiză a cărții trase
                    # S-a tras un as
                    if carte_1 == "A":
                        # Dacă total + 11 <= 21, userul poate alege as = 11 sau as = 1
                        if vg.total_blackjack + 11 <= 21:
                            message = str(user) + ", ai tras un " + carte_1 + \
                                      ". Scrie rapid „!bj 1” pentru as = 1 sau „!bj 11” pentru as = 11."

                            # Indicator că s-a tras un as
                            vg.flag_as_blackjack = True

                        # Asul e direct luat drept as = 1, în avantajul userului
                        else:
                            vg.total_blackjack += 1

                            # Userul nu a ajuns la 21
                            if vg.total_blackjack != 21:
                                message = str(user) + ", ai tras un " + carte_1 + \
                                      " (=1), ai în total " + str(vg.total_blackjack) + \
                                      ". Scrie rapid „!bj +” pentru a mai trage o carte " + \
                                      "sau „!bj stop” pentru a te opri."

                            # Userul a ajuns la 21
                            else:
                                # Cărți + total bot
                                carti_total_bot(carti)

                                # Botul nu a obținut 21
                                if vg.total_blackjack_bot != 21:
                                    if vg.miza_blackjack == 1:
                                        forma_miza = " Von"
                                    elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                        forma_miza = " Vons"
                                    else:
                                        forma_miza = " de Vons"
                                  
                                    message = str(user) + ", ai tras un " + carte_1 + " (=1), ai în total " + str(vg.total_blackjack) + \
                                              ". Ai câștigat deoarece botul a obținut " + str(vg.total_blackjack_bot) + \
                                              ". Ți-ai dublat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                              ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                                    # Acces la numărul de Vons al userului
                                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                        vg.puncte_temp_blackjack = row[0]
                                        break

                                    # Userul își primește câștigul
                                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                                   (vg.puncte_temp_blackjack + vg.miza_blackjack * 2, user))

                                    # Salvare baza de date
                                    conn.commit()

                                # Botul a obținut și el 21
                                else:
                                    if vg.miza_blackjack == 1:
                                        forma_miza = " Von"
                                    elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                        forma_miza = " Vons"
                                    else:
                                        forma_miza = " de Vons"
                                  
                                    message = str(user) + ", ai tras un " + carte_1 + " (=1), ai în total " + str(vg.total_blackjack) + \
                                              ". S-a terminat egal deoarece și botul a obținut " + str(vg.total_blackjack_bot) + \
                                              ". Ți-ai recuperat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                              ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                                    # Acces la numărul de Vons al userului
                                    for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                        vg.puncte_temp_blackjack = row[0]
                                        break

                                    # Userul își reprimește miza
                                    cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                                   (vg.puncte_temp_blackjack + vg.miza_blackjack, user))

                                    # Salvare baza de date
                                    conn.commit()

                                # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
                                reinitializare()

                    # Nu s-a tras un as
                    else:
                        # Analiză a cărții trase + calculare total
                        if nr_carte_1 >= 2 and nr_carte_1 <= 10:
                            vg.total_blackjack += nr_carte_1

                        elif nr_carte_1 > 10 and nr_carte_1 <= 13:
                            vg.total_blackjack += 10

                        # Userul nu a ajuns la 21
                        if vg.total_blackjack < 21:
                            message = str(user) + ", ai tras un " + carte_1 + \
                                      ", ai în total " + str(vg.total_blackjack) + \
                                      ". Scrie rapid „!bj +” pentru a mai trage o carte" + \
                                      " sau „!bj stop” pentru a te opri."

                        # Userul a ajuns la 21
                        elif vg.total_blackjack == 21:
                            # Cărți + total bot
                            carti_total_bot(carti)

                            # Botul nu a obținut 21
                            if vg.total_blackjack_bot != 21:
                                if vg.miza_blackjack == 1:
                                    forma_miza = " Von"
                                elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                    forma_miza = " Vons"
                                else:
                                    forma_miza = " de Vons"

                                message = str(user) + ", ai tras un " + carte_1 + ", ai în total " + str(vg.total_blackjack) + \
                                          ". Ai câștigat deoarece botul a obținut " + str(vg.total_blackjack_bot) + \
                                          ". Ți-ai dublat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                          ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                                # Acces la numărul de Vons al userului
                                for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                    vg.puncte_temp_blackjack = row[0]
                                    break

                                # Userul își primește câștigul
                                cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                               (vg.puncte_temp_blackjack + vg.miza_blackjack * 2, user))

                                # Salvare baza de date
                                conn.commit()

                            # Botul a obținut și el 21
                            else:
                                if vg.miza_blackjack == 1:
                                    forma_miza = " Von"
                                elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                    forma_miza = " Vons"
                                else:
                                    forma_miza = " de Vons"
                              
                                message = str(user) + ", ai tras un " + carte_1 + \
                                          ", ai în total " + str(vg.total_blackjack) + \
                                          ". S-a terminat egal deoarece și botul a obținut " + str(vg.total_blackjack_bot) + \
                                          ". Ți-ai recuperat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                          ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                                # Acces la numărul de Vons al userului
                                for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                                    vg.puncte_temp_blackjack = row[0]
                                    break

                                # Userul își reprimește miza
                                cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                               (vg.puncte_temp_blackjack + vg.miza_blackjack, user))

                                # Salvare baza de date
                                conn.commit()

                            # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
                            reinitializare()

                        # Userul a depășit 21
                        elif vg.total_blackjack > 21:
                            if vg.miza_blackjack == 1:
                                forma_miza = " Von"
                            elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                                forma_miza = " Vons"
                            else:
                                forma_miza = " de Vons"

                            message = str(user) + ", ai tras un " + carte_1 + ", ai în total " + str(vg.total_blackjack) + \
                                      ". Ai pierdut deoarece ai depășit 21. Ți-ai pierdut miza de " + \
                                      f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + "."

                            # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
                            reinitializare()

                    c.privmsg(self.channel, message)

                    # Aici se pune timpul de așteptare pentru pedeapsă
                    vg.pedeapsa_blackjack = time() + 40

                    # Închidere baza de date
                    conn.close()

                # Userul oprește partida
                elif alegere == "stop" and vg.flag_start_blackjack and not vg.flag_as_blackjack:
                    # Cărți + total bot
                    carti_total_bot(carti)

                    # Botul a obținut mai puțin decât userul sau a depășit 21
                    if vg.total_blackjack_bot < vg.total_blackjack or vg.total_blackjack_bot > 21:
                        if vg.miza_blackjack == 1:
                            forma_miza = " Von"
                        elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                            forma_miza = " Vons"
                        else:
                            forma_miza = " de Vons"
                      
                        message = str(user) + ", te-ai oprit la " + str(vg.total_blackjack) + \
                                  ". Ai câștigat deoarece botul a obținut " + str(vg.total_blackjack_bot) + \
                                  ". Ți-ai dublat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                  ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                        # Acces la numărul de Vons al userului
                        for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                            vg.puncte_temp_blackjack = row[0]
                            break

                        # Userul își primește câștigul
                        cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                       (vg.puncte_temp_blackjack + vg.miza_blackjack * 2, user))

                        # Salvare baza de date
                        conn.commit()

                    # Botul a obținut același total ca și userul
                    elif vg.total_blackjack_bot == vg.total_blackjack:
                        if vg.miza_blackjack == 1:
                            forma_miza = " Von"
                        elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                            forma_miza = " Vons"
                        else:
                            forma_miza = " de Vons"

                        message = str(user) + ", te-ai oprit la " + str(vg.total_blackjack) + \
                                  ". S-a terminat egal deoarece și botul a obținut " + str(vg.total_blackjack_bot) + \
                                  ". Ți-ai recuperat miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                  ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                        # Acces la numărul de Vons al userului
                        for row in cursor.execute('''SELECT puncte FROM Vons WHERE username = ?''', (user,)):
                            vg.puncte_temp_blackjack = row[0]
                            break

                        # Userul își reprimește miza
                        cursor.execute('''UPDATE Vons SET puncte = ? WHERE username = ?''',
                                       (vg.puncte_temp_blackjack + vg.miza_blackjack, user))

                        # Salvare baza de date
                        conn.commit()

                    # Botul a obținut mai mult decât userul fără să depășească 21
                    elif vg.total_blackjack_bot > vg.total_blackjack and vg.total_blackjack_bot <= 21:
                        if vg.miza_blackjack == 1:
                            forma_miza = " Von"
                        elif vg.miza_blackjack == 0 or (vg.miza_blackjack % 100 > 0 and vg.miza_blackjack % 100 < 20):
                            forma_miza = " Vons"
                        else:
                            forma_miza = " de Vons"

                        message = str(user) + ", te-ai oprit la " + str(vg.total_blackjack) + \
                                  ". Ai pierdut deoarece botul a obținut " + str(vg.total_blackjack_bot) + \
                                  ". Ți-ai pierdut miza de " + f'{numbers.format_number(vg.miza_blackjack, locale="ro_RO")}' + forma_miza + \
                                  ". Cărțile botului au fost: " + vg.carti_blackjack_bot_final + "."

                    # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
                    reinitializare()

                    c.privmsg(self.channel, message)

                    # Aici se pune timpul de așteptare pentru pedeapsă
                    vg.pedeapsa_blackjack = time() + 40

                    # Închidere baza de date
                    conn.close()

                # Comandă introdusă parțial greșit
                else:
                    # Când partida nu e începută, singura comandă posibilă e „!bj start”
                    if not vg.flag_start_blackjack:
                        message = str(user) + ", singura comandă posibilă acum e: „!bj start”."

                        vg.user_blackjack = None
                        vg.alegere_blackjack = None
                        vg.miza_blackjack = None

                    # Când s-a tras un as și userul are posibilitatea de a alege intre as = 1 și as = 11
                    # Singurele comenzi posibile sunt „!bj 1” sau „!bj 11”
                    elif vg.flag_as_blackjack:
                        message = str(user) + ", singurele comenzi posibile acum sunt: „!bj 1” sau „!bj 11”."

                    # După ce s-a tras o carte care nu e un as, singurele comenzi posibile sunt „!bj +” sau „!bj stop”
                    elif not vg.flag_as_blackjack:
                        message = str(user) + ", singurele comenzi posibile acum sunt: „!bj +” sau „!bj stop”."

                    c.privmsg(self.channel, message)

    # Comanda când e cooldown
    elif time() < vg.timp_blackjack:
        timp_ramas = int(vg.timp_blackjack - time())
        completare = "următoarea partidă de blackjack."

        vg.user_blackjack = None
        vg.alegere_blackjack = None
        vg.miza_blackjack = None
        c.privmsg(self.channel, cooldown(timp_ramas, user, completare))


# Penalizare la blackjack
def penalizare_blackjack(self, user, miza):
    c = self.connection

    if miza == 1:
        forma_miza = " Von"
    elif miza == 0 or (miza % 100 > 0 and miza % 100 < 20):
        forma_miza = " Vons"
    else:
        forma_miza = " de Vons"

    message = str(user) + ", nu ai jucat destul de repede, așa că ți-ai pierdut miza de " + \
              f'{numbers.format_number(miza, locale="ro_RO")}' + forma_miza + " prin descalificare."
    c.privmsg(self.channel, message)

    # Aici se schimbă cooldownul pentru blackjack și se reinițializează jocul
    reinitializare()


# Cărți + total bot
def carti_total_bot(carti):
    # Cât a obținut botul
    while vg.total_blackjack_bot < 17:
        nr_carte_x_bot = random.randint(2, 14)
        carte_x_bot = carti[nr_carte_x_bot]
        vg.carti_blackjack_bot.append(carte_x_bot)

        if carte_x_bot == "A":
            if vg.total_blackjack_bot + 11 <= 21:
                vg.total_blackjack_bot += 11
            else:
                vg.total_blackjack_bot += 1

        else:
            if nr_carte_x_bot >= 2 and nr_carte_x_bot <= 10:
                vg.total_blackjack_bot += nr_carte_x_bot

            elif nr_carte_x_bot > 10 and nr_carte_x_bot <= 13:
                vg.total_blackjack_bot += 10

    # Toate cărțile botului
    for i in range(len(vg.carti_blackjack_bot)):
        if i == len(vg.carti_blackjack_bot) - 1:
            vg.carti_blackjack_bot_final += "și " + vg.carti_blackjack_bot[i]
        elif i == len(vg.carti_blackjack_bot) - 2:
            vg.carti_blackjack_bot_final += vg.carti_blackjack_bot[i] + " "
        else:
            vg.carti_blackjack_bot_final += vg.carti_blackjack_bot[i] + ", "


# Jocul se reinițializează
def reinitializare():
    vg.timp_blackjack = time() + 300
    vg.user_blackjack = None
    vg.alegere_blackjack = None
    vg.miza_blackjack = None
    vg.flag_puncte_blackjack = True
    vg.flag_start_blackjack = False
    vg.flag_as_blackjack = False
    vg.puncte_temp_blackjack = None
    vg.total_blackjack = 0
    vg.total_blackjack_bot = 0
    vg.carti_blackjack_bot = []
    vg.carti_blackjack_bot_final = ""