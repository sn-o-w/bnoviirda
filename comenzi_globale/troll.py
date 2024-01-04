# Troll
def troll(self, user):
    c = self.connection

    timeout = "/timeout " + str(user) + " 30"
    c.privmsg(self.channel, timeout)