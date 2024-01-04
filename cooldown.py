def cooldown(timp_ramas, user, completare):
  # Când au rămas mai mult de 60 de secunde
  if timp_ramas >= 60:
    minute = timp_ramas // 60
    secunde = timp_ramas - minute * 60

    # Când au rămas mai multe minute
    if minute != 1:
        # Ex.: [2, 19] minute
        if minute < 20 and secunde == 0:
            message = str(user) + ", revino în {} minute pentru {}".format(minute, completare)

        # Ex.: [20, 59] de minute
        elif minute > 19 and secunde == 0:
            message = str(user) + ", revino în {} de minute pentru {}".format(minute, completare)

        # Ex.: [2, 19] minute și 1 secundă
        elif minute < 20 and secunde == 1:
            message = str(user) + ", revino în {} minute și 1 secundă pentru {}".format(minute, completare)

        # Ex.: [20, 59] de minute și 1 secundă
        elif minute > 19 and secunde == 1:
            message = str(user) + ", revino în {} de minute și 1 secundă pentru {}".format(minute, completare)

        # Ex.: [2, 19] minute și [2, 19] secunde
        elif minute < 20 and secunde < 20 and secunde != 0:
            message = str(user) + ", revino în {} minute și {} secunde pentru {}".format(minute, secunde, completare)

        # Ex.: [2, 19] minute și [20, 59] de secunde
        elif minute < 20 and secunde > 19 and secunde != 0:
            message = str(user) + ", revino în {} minute și {} de secunde pentru {}".format(minute, secunde, completare)

        # Ex.: [20, 59] de minute și [2, 19] secunde
        elif minute > 19 and secunde < 20 and secunde != 0:
            message = str(user) + ", revino în {} de minute și {} secunde pentru {}".format(minute, secunde, completare)

        # Ex.: [20, 59] de minute și [20, 59] de secunde
        elif minute > 19 and secunde > 19 and secunde != 0:
            message = str(user) + ", revino în {} de minute și {} de secunde pentru {}".format(minute, secunde, completare)

    # Când a rămas doar 1 minut
    else:
        # Ex.: 1 minut
        if secunde == 0:
            message = str(user) + ", revino într-un minut pentru {}".format(completare)

        # Ex.: 1 minut și 1 secundă
        elif secunde == 1:
            message = str(user) + ", revino într-un minut și {} secundă pentru {}".format(secunde, completare)

        # Ex.: 1 minut și [2, 19] secunde
        elif secunde < 20:
            message = str(user) + ", revino într-un minut și {} secunde pentru {}".format(secunde, completare)

        # Ex.: 1 minut și [20, 59] de secunde
        else:
            message = str(user) + ", revino într-un minut și {} de secunde pentru {}".format(secunde, completare)

  # Când au rămas mai puțin de 60 de secunde
  else:
    # Ex.: 1 secundă
    if timp_ramas == 1:
        message = str(user) + ", revino într-o secundă pentru {}".format(completare)

    # Ex.: [2, 19] secunde
    elif timp_ramas < 20:
        message = str(user) + ", revino în {} secunde pentru {}".format(timp_ramas, completare)

    # Ex.: [20, 59] de secunde
    else:
        message = str(user) + ", revino în {} de secunde pentru {}".format(timp_ramas, completare)

  return message