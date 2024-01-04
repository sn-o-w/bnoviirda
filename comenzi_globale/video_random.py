# Imports
import sys, random
sys.path.append("..")
import variabile_globale as vg
from time import time
from cooldown import cooldown

# Video random
def video_random(self, user):
    c = self.connection

    # Comanda când nu e cooldown
    if time() >= vg.timp_video:
        lista_video = ["https://clips.twitch.tv/EmpathicLazyPotatoBabyRage",
                       "https://clips.twitch.tv/BelovedCallousZebraTinyFace",
                        "https://clips.twitch.tv/SnappyBlindingSpaghettiKlappa",
                        "https://clips.twitch.tv/GiftedAthleticLemurUncleNox",
                        "https://clips.twitch.tv/FunnyHardTrayTwitchRPG",
                        "https://clips.twitch.tv/ModernJazzyCrowCoolStoryBob",
                        "https://clips.twitch.tv/MotionlessProtectiveIcecreamMikeHogu",
                        "https://clips.twitch.tv/ExpensiveCallousWhalePeoplesChamp",
                        "https://clips.twitch.tv/YawningFitFennelKAPOW",
                        "https://clips.twitch.tv/CooperativeBigStingrayAMPTropPunch",
                        "https://clips.twitch.tv/AmorphousSmokyPeppermintTBTacoRight",
                        "https://clips.twitch.tv/ArbitraryIncredulousKoupreyAMPEnergyCherry",
                        "https://clips.twitch.tv/UnsightlyJoyousPepperDeIlluminati",
                        "https://clips.twitch.tv/HyperWanderingTurnipMoreCowbell",
                        "https://clips.twitch.tv/BloodyBeautifulSushiHumbleLife",
                        "https://clips.twitch.tv/BrainyWanderingDillPunchTrees",
                        "https://clips.twitch.tv/FunnyStrangeLettuceCoolStoryBro",
                        "https://clips.twitch.tv/DeliciousAlertOxOMGScoots",
                        "https://clips.twitch.tv/SpinelessSwissOcelotTF2John",
                        "https://clips.twitch.tv/MistyCrackyMeatloafKippa",
                        "https://clips.twitch.tv/TangentialSmellyTurnipRuleFive",
                        "https://clips.twitch.tv/AbstemiousPowerfulLatteWholeWheat",
                        "https://clips.twitch.tv/VivaciousMagnificentSnailNerfRedBlaster",
                        "https://clips.twitch.tv/SuaveSaltyAniseJKanStyle",
                        "https://clips.twitch.tv/ObservantSarcasticWoodpeckerBloodTrail",
                        "https://clips.twitch.tv/WittyCallousAntelopeAllenHuhu",
                        "https://clips.twitch.tv/PiliablePiercingWormAMPEnergyCherry",
                        "https://clips.twitch.tv/TsundereNeighborlySandpiperGOWSkull",
                        "https://clips.twitch.tv/FreezingFurryPastaGOWSkull",
                        "https://clips.twitch.tv/FilthyImpossibleHummingbirdPoooound",
                        "https://clips.twitch.tv/TastyAmericanAyeayeThunBeast-3m44KqWyzD2Jdu2o",
                        "https://clips.twitch.tv/PowerfulCredulousOysterUncleNox-IJTwU79E6SJyEWjk",
                        "https://clips.twitch.tv/ResilientJoyousVampireJebaited--E_k9FRZbQeiiXGV",
                        "https://clips.twitch.tv/SmallDullFlyAMPEnergyCherry-lpM0ASuXdAc_rlUl",
                        "https://clips.twitch.tv/PrettiestCleverPieMoreCowbell-lPbzdthugKWuB9v-",
                        "https://clips.twitch.tv/PreciousFastWolverineBIRB-eAQPe25sQU1LaFpI",
                        "https://clips.twitch.tv/AgreeableAbnegateHamAliens-6fXnH6Bw-hTHEMwu",
                        "https://clips.twitch.tv/PhilanthropicResilientRedpandaKlappa-eth-LioTLTq9DSuA",
                        "https://clips.twitch.tv/InquisitiveGiantFalconAMPEnergyCherry-Ps0JqTwd2LFVzyY3",
                        "https://clips.twitch.tv/DrabSpookyBaboonTBTacoRight-VpMj3MHvP8_O3aMh",
                        "https://clips.twitch.tv/ManlyCarefulGarageKreygasm-rODD8ZH79oNT-h-m",
                        "https://clips.twitch.tv/AgreeableGoldenIcecreamBIRB-7ph_Pea2RG8ojCFi",
                        "https://clips.twitch.tv/SuaveSassyOctopusBCWarrior-be-MzIq9wov4s-Lb",
                        "https://clips.twitch.tv/SuperPricklySpaghettiPlanking-CmUY3vKDpw0ud7t9",
                        "https://clips.twitch.tv/TameOptimisticTireBlargNaut-BTc2S-W-a7EFFluL",
                        "https://clips.twitch.tv/BeautifulTolerantCougarMingLee-VzZVZ6pHu35FHLex",
                        "https://clips.twitch.tv/AdventurousAmorphousLionKappaRoss-YFS1rKSLaWTX1IwV"]

        # Se alege un video random
        numar_video = random.randint(0, len(lista_video) - 1)

        message = lista_video[numar_video]
        c.privmsg(self.channel, message)

        # Cooldown
        vg.timp_video = time() + 30

    # Comanda când e cooldown
    elif time() < vg.timp_video:
        timp_ramas = int(vg.timp_video - time())
        completare = "următorul video random."

        c.privmsg(self.channel, cooldown(timp_ramas, user, completare))