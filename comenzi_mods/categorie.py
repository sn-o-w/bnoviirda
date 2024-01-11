# Schimbă categoria
def mods_schimba_categoria(self, categorie, mod):
    c = self.connection

    # "prescurtare" : "mesaj pe care botul îl va trimite în chat",
    categorii = {"jc" : "!game Just Chatting",
                 "tft" : "!game Teamfight Tactics",
                 "m" : "!game Marbles on Stream",
                 "v" : "!game VALORANT",
                 "cs" : "!game Counter-Strike", # RIP CS:GO
                 "irl" : "!game Travel & Outdoors",
                 "cook" : "!game Food & Drink",
                 "lol" : "!game League of Legends",
                 "he" : "!game Hercules",
                 "gg" : "!game GeoGuessr",
                 "jk" : "!game Jump King",
                 "medan" : "!game The Dark Pictures Anthology: Man of Medan",
                 "bomb" : "!game Bombergrounds: Battle Royale",
                 "tt" : "!game Tricky Towers",
                 "cod" : "!game Call of Duty: Warzone",
                 "forza": "!game Forza Horizon 5",
                 "raft": "!game Raft",
                 "tavern": "!game Tavern Master",
                 "fort": "!game Fortnite",
                 "mp" : "!game Monopoly Plus"}

    # Comandă + categorie care există
    if categorie in categorii.keys():
        message = categorii[categorie]

    # Comandă fără categorie
    elif categorie is None:
        message = str(mod) + ", trebuie aleasă și o categorie."

    # Comandă + categorie greșită
    elif categorie not in categorii.keys():
        # Încearcă să găsească cea mai apropiată categorie existentă
        temp = []
        for key, val in categorii.items():
            if categorie[0] == key[0]:
                temp.append((key, val))

        # Nu a fost găsită nici o categorie apropiată
        if temp == []:
            message = str(mod) + ", această categorie încă nu a fost adăugată în memoria mea sau ai greșit comanda."

        # A fost găsită cel puțin o categorie apropiată
        else:
            # A fost găsită doar o categorie apropiată
            if len(temp) == 1:
                message = str(mod) + ", varianta cea mai apropiată e: " + "!g " + temp[0][0] + " -> " + temp[0][1]

            # Au fost găsite mai multe categorii apropiate
            else:
                message = str(mod) + ", variantele cele mai apropiate sunt: "
                for i in range(len(temp)):
                    message += "!g " + temp[i][0] + " -> " + temp[i][1]

                    if i != len(temp) - 1:
                        message += ", "

    c.privmsg(self.channel, message)