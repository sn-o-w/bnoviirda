def cooldown(timp_ramas, user, completare):
    minute = timp_ramas // 60
    secunde = timp_ramas % 60

    if minute == 1:
        forma_minute = "minut"
    elif minute == 0 or (minute % 100 > 0 and minute % 100 < 20):
        forma_minute = "minute"
    else:
        forma_minute = "de minute"

    if secunde == 1:
        forma_secunde = "secundă"
    elif secunde == 0 or (secunde % 100 > 0 and secunde % 100 < 20):
        forma_secunde = "secunde"
    else:
        forma_secunde = "de secunde"

    if minute == 1 and secunde:
        message = "{}, revino într-un {} și {} {} pentru {}".format(user, forma_minute, secunde, forma_secunde, completare)
    elif minute > 1 and secunde:
        message = "{}, revino în {} {} și {} {} pentru {}".format(user, minute, forma_minute, secunde, forma_secunde, completare)
    elif minute == 1:
        message = "{}, revino într-un {} pentru {}".format(user, forma_minute, completare)
    elif minute:
        message = "{}, revino în {} {} pentru {}".format(user, minute, forma_minute, completare)
    elif secunde == 1:
        message = "{}, revino într-o {} pentru {}".format(user, forma_secunde, completare)
    else:
        message = "{}, revino în {} {} pentru {}".format(user, secunde, forma_secunde, completare)

    return message