# Imports
import random

# Comandă de love
def love(self, pers1, pers2):
    c = self.connection

    # Comandă + mention
    if pers2 is not None:
        procent = random.randint(0, 100)

        # ZULULW
        if str(pers1) == "marian2407" and str(pers2) == "adriivonb":
            message = str(pers1) + " și " + str(pers2) + " se iubesc în proporție de 0% adriiv1Spit"

        else:
            message = str(pers1) + " și " + str(pers2) + " se iubesc în proporție de " + str(procent) + "% adriiv1L"

    # Comandă fără mention
    else:
        message = str(pers1) + ", trebuie să dai mention unei persoane."

    c.privmsg(self.channel, message)