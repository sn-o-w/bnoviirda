# Imports
from datetime import datetime
import pytz

def calcul_varsta(data_de_start):
    data_in_prezent = datetime.now(pytz.timezone('Europe/Bucharest'))
    diferenta = data_in_prezent.year - data_de_start.year
    if (data_de_start.month > data_in_prezent.month) or ((data_de_start.month == data_in_prezent.month) and (data_de_start.day > data_in_prezent.day)):
        diferenta -= 1
    return diferenta

data_de_start = datetime.strptime('1999-07-31', '%Y-%m-%d')
varsta = calcul_varsta(data_de_start)

# Întrebări
def intrebari(self, cmd, nume):
    c = self.connection

    # La ce facultate e
    if cmd == "facultate":
        # Comandă + mention
        if nume is not None:
            message = str(nume) + ", Contabilitate și Informatică de Gestiune în cadrul" \
                      + " Academiei de Studii Economice din București adriiv1Afaceri"

        # Comandă fără mention
        else:
            message = "Contabilitate și Informatică de Gestiune în cadrul" \
                      + " Academiei de Studii Economice din București adriiv1Afaceri"

    # Ce înălțime are
    elif cmd == "inaltime":
        # Comandă + mention
        if nume is not None:
            message = str(nume) + ", am 1,59, dar am uitat să modific în descriere adriiv1W"

        # Comandă fără mention
        else:
            message = "Am 1,59, dar am uitat să modific în descriere adriiv1W"

    # Câți ani are
    elif cmd == "ani":
        # Comandă + mention
        if nume is not None:
            message = str(nume) + ", chatul va spune 15, dar descrierea altceva," \
                      + " deci mai bine verifici tu (pe scurt, " + f'{varsta}' + ") adriiv1W"

        # Comandă fără mention
        else:
            message = "Chatul va spune 15, dar descrierea altceva," \
                      + " deci mai bine verifici tu (pe scurt, " + f'{varsta}' + ") adriiv1W"

    # De când a început să facă stream
    elif cmd == "inceput":
        # Comandă + mention
        if nume is not None:
            message = str(nume) + ", m-am apucat de stream în noiembrie 2019 adriiv1W"

        # Comandă fără mention
        else:
            message = "M-am apucat de stream în noiembrie 2019 adriiv1W"

    # Ce zodie e
    elif cmd == "zodie":
        # Comandă + mention
        if nume is not None:
            message = str(nume) + ", sunt zodia leu, este și în descriere, plus alte informații despre mine adriiv1Cute"

        # Comandă fără mention
        else:
            message = "Sunt zodia leu, este și în descriere, plus alte informații despre mine adriiv1Cute"

    c.privmsg(self.channel, message)