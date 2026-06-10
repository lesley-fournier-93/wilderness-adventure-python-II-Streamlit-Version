# Portfolio-Projekt: Abenteuer in der Wildnis
# Datei: wildnis_core.py
# Hier steht nur die Spiellogik.
# Keine input()-Abfragen und kein Tkinter.

import json
import os
import random
from datetime import datetime


# --------------------------------------------------
# Aufgabe 1: Gegenstand
# --------------------------------------------------

class Gegenstand:
    def __init__(self, name, menge):
        self.name = name.title()
        self.menge = int(menge)

    def beschreibung(self):
        return f"{self.menge}x {self.name}"


# --------------------------------------------------
# Aufgabe 2 und 3: Inventar
# --------------------------------------------------

class Inventar:
    def __init__(self):
        self.gegenstaende = []
        self.obergrenze = 200

    def hinzufuegen(self, item):
        if type(item) != Gegenstand:
            return False, "Fehler: Das ist kein Gegenstand."

        if self.gesamtmenge() + item.menge > self.obergrenze:
            return False, "Fehler: Inventar-Obergrenze erreicht."

        for i in self.gegenstaende:
            if i.name.title() == item.name.title():
                i.menge += item.menge
                return True, f"Inventar: +{item.menge} {item.name}"

        self.gegenstaende.append(item)
        return True, f"Inventar: +{item.menge} {item.name}"

    def anzeigen(self):
        if len(self.gegenstaende) == 0:
            return "Inventar ist leer."

        ausgabe = []
        for i in self.gegenstaende:
            ausgabe.append(i.beschreibung())

        return "\n".join(ausgabe)

    def als_liste(self):
        liste = []
        for item in self.gegenstaende:
            liste.append((item.name, item.menge))
        return liste

    def gesamtmenge(self):
        gesamt = 0
        for i in self.gegenstaende:
            gesamt += i.menge
        return gesamt

    def suchen(self, name):
        for i in self.gegenstaende:
            if i.name.title() == name.title():
                return i
        return None

    def besitzt(self, name, menge):
        item = self.suchen(name)

        if item == None:
            return False

        if item.menge < int(menge):
            return False

        return True

    def entfernen(self, name, menge):
        menge = int(menge)
        item = self.suchen(name)

        if item == None:
            return False, f"{name.title()} ist nicht im Inventar."

        if item.menge < menge:
            return False, f"Nicht genug {name.title()} vorhanden."

        item.menge -= menge

        if item.menge == 0:
            self.gegenstaende.remove(item)

        return True, f"Inventar: -{menge} {name.title()}"


# --------------------------------------------------
# Status-Klasse
# --------------------------------------------------

class Status:
    def __init__(self, gesundheit, energie):
        self.gesundheit = int(gesundheit)
        self.energie = int(energie)
        self.max_gesundheit = 100
        self.max_energie = 100

    def anzeige(self):
        return f"Gesundheit: {self.gesundheit}, Energie: {self.energie}"

    def energie_verbrauchen(self, menge):
        alte_energie = self.energie
        self.energie -= int(menge)

        if self.energie <= 0:
            self.energie = 0

        verbraucht = alte_energie - self.energie
        return verbraucht

    def heilen(self, menge):
        alte_gesundheit = self.gesundheit
        self.gesundheit += int(menge)

        if self.gesundheit > self.max_gesundheit:
            self.gesundheit = self.max_gesundheit

        return self.gesundheit - alte_gesundheit

    def energie_geben(self, menge):
        alte_energie = self.energie
        self.energie += int(menge)

        if self.energie > self.max_energie:
            self.energie = self.max_energie

        return self.energie - alte_energie

    def schaden_nehmen(self, menge):
        alte_gesundheit = self.gesundheit
        self.gesundheit -= int(menge)

        if self.gesundheit <= 0:
            self.gesundheit = 0

        return alte_gesundheit - self.gesundheit

    def ruhe(self):
        alte_gesundheit = self.gesundheit
        alte_energie = self.energie

        self.energie = self.max_energie
        self.heilen(20)

        neue_gesundheit = self.gesundheit - alte_gesundheit
        neue_energie = self.energie - alte_energie

        return neue_gesundheit, neue_energie


# --------------------------------------------------
# Aufgabe 4: Charakter
# --------------------------------------------------

class Charakter:
    def __init__(self, name, gesundheit, energie):
        self.name = name.title()
        self.inventar = Inventar()
        self.status = Status(gesundheit, energie)

    def gegenstand_hinzufuegen(self, item):
        return self.inventar.hinzufuegen(item)

    def gegenstand_entfernen(self, name, menge):
        return self.inventar.entfernen(name, menge)

    def inventar_anzeigen(self):
        return f"Inventar von {self.name}:\n{self.inventar.anzeigen()}"

    def status_anzeige(self):
        return f"Status von {self.name}:\n{self.status.anzeige()}"

    def warnung_pruefen(self):
        warnungen = []

        if self.status.gesundheit <= 30 and self.status.gesundheit > 0:
            warnungen.append(f"WARNUNG: Deine Gesundheit ist niedrig. {self.name} sollte essen, Kräuter nutzen oder schlafen.")

        if self.status.energie <= 30 and self.status.energie > 0:
            warnungen.append(f"WARNUNG: Deine Energie ist niedrig. {self.name} sollte bald schlafen oder etwas essen.")

        return "\n".join(warnungen)

    def aktion_ausfuehren(self, aktion, kosten):
        if self.status.energie == 0:
            return False, f"{self.name} kann keine Aktion mehr ausführen. Energie erschöpft!"

        if self.status.gesundheit == 0:
            return False, f"{self.name} kann keine Aktion mehr ausführen. Gesundheit erschöpft!"

        meldung = []
        meldung.append(f"{self.name} führt die Aktion aus: {aktion}")

        verbrauchte_energie = self.status.energie_verbrauchen(kosten)
        meldung.append(f"Energie: -{verbrauchte_energie}")

        if self.status.energie > 0:
            meldung.append("Aktion erfolgreich.")
        else:
            meldung.append("Energie erschöpft!")

        meldung.append(self.status_anzeige())

        warnung = self.warnung_pruefen()
        if warnung != "":
            meldung.append(warnung)

        return True, "\n".join(meldung)

    def nacht_durchschlafen(self):
        neue_gesundheit, neue_energie = self.status.ruhe()

        meldung = []
        meldung.append(f"{self.name} geht jetzt schlafen.")
        meldung.append("Eine ruhige Nacht gibt neue Kraft.")
        meldung.append(f"{self.name} ist erholt und startet in den nächsten Tag.")
        meldung.append(f"Gesundheit: +{neue_gesundheit}")
        meldung.append(f"Energie: +{neue_energie}")
        meldung.append(self.status_anzeige())

        warnung = self.warnung_pruefen()
        if warnung != "":
            meldung.append(warnung)

        return "\n".join(meldung)


# --------------------------------------------------
# Aufgabe 5: Handelssystem
# --------------------------------------------------

def handel(char1, char2, gegenstand_char1, gegenstand_char2, zustimmung_char1, zustimmung_char2):
    if zustimmung_char1 == False or zustimmung_char2 == False:
        return False, "Handel abgebrochen: Nicht beide Charaktere haben zugestimmt."

    if type(gegenstand_char1) != Gegenstand or type(gegenstand_char2) != Gegenstand:
        return False, "Fehler: Es können nur Gegenstände gehandelt werden."

    if char1.inventar.besitzt(gegenstand_char1.name, gegenstand_char1.menge) == False:
        return False, f"Handel abgebrochen: {char1.name} besitzt nicht genug {gegenstand_char1.name}."

    if char2.inventar.besitzt(gegenstand_char2.name, gegenstand_char2.menge) == False:
        return False, f"Handel abgebrochen: {char2.name} besitzt nicht genug {gegenstand_char2.name}."

    neue_menge_char1 = char1.inventar.gesamtmenge() - gegenstand_char1.menge + gegenstand_char2.menge
    neue_menge_char2 = char2.inventar.gesamtmenge() - gegenstand_char2.menge + gegenstand_char1.menge

    if neue_menge_char1 > char1.inventar.obergrenze:
        return False, f"Handel abgebrochen: Das Inventar von {char1.name} wäre zu voll."

    if neue_menge_char2 > char2.inventar.obergrenze:
        return False, f"Handel abgebrochen: Das Inventar von {char2.name} wäre zu voll."

    char1.inventar.entfernen(gegenstand_char1.name, gegenstand_char1.menge)
    char2.inventar.entfernen(gegenstand_char2.name, gegenstand_char2.menge)

    char2.inventar.hinzufuegen(gegenstand_char1)
    char1.inventar.hinzufuegen(gegenstand_char2)

    meldung = []
    meldung.append("Handel erfolgreich!")
    meldung.append("Nach dem Tausch:")
    meldung.append(char1.inventar_anzeigen())
    meldung.append("")
    meldung.append(char2.inventar_anzeigen())

    return True, "\n".join(meldung)


# --------------------------------------------------
# Zusatzfunktion: Signalfeuer
# --------------------------------------------------

def signalfeuer_bauen(charakter):
    meldung = []
    meldung.append(f"{charakter.name} versucht, ein großes Signalfeuer zu bauen.")

    if (
        charakter.inventar.besitzt("Holz", 100)
        and charakter.inventar.besitzt("Stein", 30)
        and charakter.inventar.besitzt("Fisch", 5)
        and charakter.inventar.besitzt("Harz", 3)
        and charakter.inventar.besitzt("Feuerstein", 1)
        and charakter.inventar.besitzt("Stoff", 2)
    ):
        charakter.inventar.entfernen("Holz", 100)
        charakter.inventar.entfernen("Stein", 30)
        charakter.inventar.entfernen("Fisch", 5)
        charakter.inventar.entfernen("Harz", 3)
        charakter.inventar.entfernen("Feuerstein", 1)
        charakter.inventar.entfernen("Stoff", 2)

        meldung.append(f"{charakter.name} legt Holz und Steine zu einer sicheren Feuerstelle.")
        meldung.append("Mit Harz, Feuerstein und Stoff entzündet er ein starkes Signalfeuer.")
        meldung.append("Der Rauch steigt hoch in den Himmel.")
        meldung.append("Tesla sieht den Rauch und ruft um Hilfe.")
        meldung.append("Ein Rettungsteam entdeckt das Signal.")
        meldung.append("GEWONNEN!")
        meldung.append(f"{charakter.name} wurde gerettet.")
        return True, "\n".join(meldung)

    meldung.append(f"{charakter.name} hat noch nicht genug Materialien.")
    meldung.append("Für das Signalfeuer braucht er:")
    meldung.append("100x Holz")
    meldung.append("30x Stein")
    meldung.append("5x Fisch")
    meldung.append("3x Harz")
    meldung.append("1x Feuerstein")
    meldung.append("2x Stoff")
    meldung.append("Tipp: Holz, Stein und Fisch kann der Spieler selbst sammeln.")
    meldung.append("Harz, Feuerstein und Stoff bekommt er nur bei Tesla, der Händlerin.")

    return False, "\n".join(meldung)


# --------------------------------------------------
# Bestenliste
# --------------------------------------------------

class Bestenliste:
    def __init__(self, dateiname="bestenliste.json"):
        self.dateiname = dateiname

    def laden(self):
        if os.path.exists(self.dateiname) == False:
            return []

        try:
            with open(self.dateiname, "r", encoding="utf-8") as datei:
                return json.load(datei)
        except json.JSONDecodeError:
            return []

    def speichern(self, eintraege):
        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(eintraege, datei, indent=4, ensure_ascii=False)

    def eintrag_hinzufuegen(self, name, punkte, gewonnen, runden):
        eintraege = self.laden()

        eintrag = {
            "name": name,
            "punkte": punkte,
            "gewonnen": gewonnen,
            "runden": runden,
            "datum": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        eintraege.append(eintrag)
        eintraege = sorted(eintraege, key=lambda x: x["punkte"], reverse=True)
        eintraege = eintraege[:10]
        self.speichern(eintraege)

    def anzeigen(self):
        eintraege = self.laden()

        if len(eintraege) == 0:
            return "Noch keine Einträge in der Bestenliste."

        ausgabe = []
        ausgabe.append("BESTENLISTE")
        ausgabe.append("======================================")

        platz = 1
        for eintrag in eintraege:
            status = "Gewonnen" if eintrag["gewonnen"] == True else "Beendet"
            ausgabe.append(
                f"{platz}. {eintrag['name']} | {eintrag['punkte']} Punkte | {eintrag['runden']} Runden | {status} | {eintrag['datum']}"
            )
            platz += 1

        return "\n".join(ausgabe)


# --------------------------------------------------
# Spiel-Verwaltung
# --------------------------------------------------

class AbenteuerSpiel:
    def __init__(self, spielername):
        if spielername.strip() == "":
            spielername = "Edison"

        self.spielername = spielername.strip().title()
        self.spieler = Charakter(self.spielername, 100, 100)
        self.tesla = Charakter("Tesla", 100, 100)
        self.runden = 0
        self.gewonnen = False
        self.game_over = False
        self.beendet = False
        self.bestenliste = Bestenliste()
        self.startinventar_anlegen()

    def startinventar_anlegen(self):
        self.spieler.gegenstand_hinzufuegen(Gegenstand("Holz", 40))
        self.spieler.gegenstand_hinzufuegen(Gegenstand("Stein", 10))
        self.spieler.gegenstand_hinzufuegen(Gegenstand("Beeren", 2))

        self.tesla.gegenstand_hinzufuegen(Gegenstand("Harz", 10))
        self.tesla.gegenstand_hinzufuegen(Gegenstand("Feuerstein", 5))
        self.tesla.gegenstand_hinzufuegen(Gegenstand("Stoff", 6))
        self.tesla.gegenstand_hinzufuegen(Gegenstand("Nüsse", 10))
        self.tesla.gegenstand_hinzufuegen(Gegenstand("Kräuter", 8))

    def intro_text(self):
        return (
            "======================================\n"
            "ABENTEUER IN DER WILDNIS\n"
            "======================================\n\n"
            f"Nach einem schweren Sturm wacht {self.spielername} allein in der Wildnis auf.\n"
            "Das Lager ist zerstört und der Rückweg ist versperrt.\n"
            "In der Ferne sieht man ein kleines Häuschen.\n"
            "Dort lebt Tesla, eine kluge Händlerin, die seltene Materialien besitzt.\n"
            f"{self.spielername} muss sammeln, essen, handeln, schlafen und überleben.\n"
            "Das Ziel: Ein großes Signalfeuer bauen, damit die Rettung kommt.\n\n"
            "Startstatus:\n"
            f"{self.spieler.status_anzeige()}\n\n"
            "Startinventar:\n"
            f"{self.spieler.inventar_anzeigen()}"
        )

    def status_text(self):
        text = self.spieler.status_anzeige()
        warnung = self.spieler.warnung_pruefen()
        if warnung != "":
            text += "\n" + warnung
        return text

    def inventar_text(self):
        return self.spieler.inventar_anzeigen()

    def tesla_inventar_text(self):
        return self.tesla.inventar_anzeigen()

    def runde_zaehlen(self):
        self.runden += 1

    def punkte_berechnen(self):
        punkte = self.spieler.status.gesundheit + self.spieler.status.energie
        punkte += self.spieler.inventar.gesamtmenge()
        punkte -= self.runden * 2

        if self.gewonnen == True:
            punkte += 500

        if punkte < 0:
            punkte = 0

        return punkte

    def spiel_beenden(self):
        if self.beendet == True:
            return "Das Spiel ist bereits beendet."

        self.beendet = True
        punkte = self.punkte_berechnen()
        self.bestenliste.eintrag_hinzufuegen(self.spielername, punkte, self.gewonnen, self.runden)

        if self.gewonnen == True:
            ergebnis = f"SPIEL BEENDET: {self.spielername} wurde gerettet."
        elif self.game_over == True:
            ergebnis = "SPIEL BEENDET: Abenteuer gescheitert."
        else:
            ergebnis = f"SPIEL BEENDET: {self.spielername} hat den Tag überlebt."

        return f"{ergebnis}\nPunkte: {punkte}\n\nEndstatus:\n{self.spieler.status_anzeige()}\n\nEndinventar:\n{self.spieler.inventar_anzeigen()}"

    def game_over_pruefen(self):
        if self.spieler.status.gesundheit == 0:
            self.game_over = True
            return "GAME OVER!\nDer Spieler ist leider gestorben."

        if self.spieler.status.energie == 0:
            return f"{self.spielername} hat keine Energie mehr. Das Abenteuer ist für heute vorbei."

        if self.gewonnen == True:
            return "Das Spiel ist gewonnen."

        return ""

    def zufallsereignis_pruefen(self):
        zahl = random.randint(1, 100)

        if zahl <= 12:
            schaden = random.randint(5, 15)
            verloren = self.spieler.status.schaden_nehmen(schaden)
            return f"Zufallsereignis: Ein Dornenbusch verletzt {self.spielername}. Gesundheit: -{verloren}"

        if zahl <= 22:
            fund = random.choice([
                Gegenstand("Beeren", random.randint(1, 3)),
                Gegenstand("Holz", random.randint(5, 15)),
                Gegenstand("Stein", random.randint(2, 8))
            ])
            self.spieler.gegenstand_hinzufuegen(fund)
            return f"Zufallsereignis: {self.spielername} findet unterwegs {fund.beschreibung()}."

        return ""

    def aktion_abschliessen(self, meldung):
        if self.beendet == False and self.gewonnen == False:
            zufall = self.zufallsereignis_pruefen()
            if zufall != "":
                meldung += "\n\n" + zufall

        pruefung = self.game_over_pruefen()
        if pruefung != "":
            meldung += "\n\n" + pruefung
            meldung += "\n\n" + self.spiel_beenden()

        return meldung

    def holz_sammeln(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Holz sammeln", 20)
        if erfolg == True:
            menge = random.randint(20, 40)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Holz", menge))
            meldung += f"\nInventar: +{menge} Holz"
        return self.aktion_abschliessen(meldung)

    def steine_sammeln(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Steine sammeln", 25)
        if erfolg == True:
            menge = random.randint(10, 25)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Stein", menge))
            meldung += f"\nInventar: +{menge} Stein"
        return self.aktion_abschliessen(meldung)

    def angeln_gehen(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Angeln gehen", 30)
        if erfolg == True:
            menge = random.randint(2, 6)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Fisch", menge))
            meldung += f"\nInventar: +{menge} Fisch"
        return self.aktion_abschliessen(meldung)

    def fluss_ueberqueren(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Fluss überqueren", 40)
        if erfolg == True:
            schaden = random.randint(30, 55)
            verloren = self.spieler.status.schaden_nehmen(schaden)
            meldung += f"\nDer Fluss ist reißend. {self.spielername} verletzt sich.\nGesundheit: -{verloren}"
        return self.aktion_abschliessen(meldung)

    def beeren_sammeln(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Beeren sammeln", 10)
        if erfolg == True:
            menge = random.randint(1, 5)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Beeren", menge))
            meldung += f"\nInventar: +{menge} Beeren"
        return self.aktion_abschliessen(meldung)

    def nuesse_sammeln(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Nüsse sammeln", 15)
        if erfolg == True:
            menge = random.randint(1, 4)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Nüsse", menge))
            meldung += f"\nInventar: +{menge} Nüsse"
        return self.aktion_abschliessen(meldung)

    def kraeuter_suchen(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Kräuter suchen", 15)
        if erfolg == True:
            menge = random.randint(1, 3)
            self.spieler.gegenstand_hinzufuegen(Gegenstand("Kräuter", menge))
            meldung += f"\nInventar: +{menge} Kräuter"
        return self.aktion_abschliessen(meldung)

    def schlafen(self):
        self.runde_zaehlen()
        meldung = self.spieler.nacht_durchschlafen()
        return self.aktion_abschliessen(meldung)

    def essen(self, nahrung):
        self.runde_zaehlen()

        if nahrung == "Beeren":
            erfolg, meldung = self.spieler.aktion_ausfuehren("Beeren essen", 5)
            if erfolg == True:
                ok, info = self.spieler.inventar.entfernen("Beeren", 1)
                if ok == True:
                    plus = self.spieler.status.heilen(20)
                    meldung += f"\n{self.spielername} isst Beeren.\nGesundheit: +{plus}"
                else:
                    meldung += "\n" + info
            return self.aktion_abschliessen(meldung)

        if nahrung == "Fisch":
            erfolg, meldung = self.spieler.aktion_ausfuehren("Fisch essen", 5)
            if erfolg == True:
                ok, info = self.spieler.inventar.entfernen("Fisch", 1)
                if ok == True:
                    plus_hp = self.spieler.status.heilen(25)
                    plus_en = self.spieler.status.energie_geben(10)
                    meldung += f"\n{self.spielername} isst Fisch.\nGesundheit: +{plus_hp}\nEnergie: +{plus_en}"
                else:
                    meldung += "\n" + info
            return self.aktion_abschliessen(meldung)

        if nahrung == "Nüsse":
            erfolg, meldung = self.spieler.aktion_ausfuehren("Nüsse essen", 5)
            if erfolg == True:
                ok, info = self.spieler.inventar.entfernen("Nüsse", 1)
                if ok == True:
                    plus = self.spieler.status.energie_geben(20)
                    meldung += f"\n{self.spielername} isst Nüsse.\nEnergie: +{plus}"
                else:
                    meldung += "\n" + info
            return self.aktion_abschliessen(meldung)

        if nahrung == "Kräuter":
            erfolg, meldung = self.spieler.aktion_ausfuehren("Kräuter nutzen", 5)
            if erfolg == True:
                ok, info = self.spieler.inventar.entfernen("Kräuter", 1)
                if ok == True:
                    plus = self.spieler.status.heilen(15)
                    meldung += f"\n{self.spielername} nutzt Kräuter.\nGesundheit: +{plus}"
                else:
                    meldung += "\n" + info
            return self.aktion_abschliessen(meldung)

        return "Diese Nahrung gibt es nicht."

    def handel_mit_tesla(self, name_spieler, menge_spieler, name_tesla, menge_tesla):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Zu Teslas Häuschen gehen", 10)

        if erfolg == False:
            return self.aktion_abschliessen(meldung)

        try:
            menge_spieler = int(menge_spieler)
            menge_tesla = int(menge_tesla)
        except ValueError:
            return "Bitte gib bei den Mengen Zahlen ein."

        gegenstand_spieler = Gegenstand(name_spieler, menge_spieler)
        gegenstand_tesla = Gegenstand(name_tesla, menge_tesla)

        handels_erfolg, handels_meldung = handel(
            self.spieler,
            self.tesla,
            gegenstand_spieler,
            gegenstand_tesla,
            True,
            True
        )

        meldung += "\n\nTesla tritt aus ihrem kleinen Häuschen."
        meldung += "\nSeltene Materialien bekommst du nur durch Handel."
        meldung += "\n\n" + handels_meldung

        return self.aktion_abschliessen(meldung)

    def signalfeuer(self):
        self.runde_zaehlen()
        erfolg, meldung = self.spieler.aktion_ausfuehren("Signalfeuer bauen", 30)

        if erfolg == True:
            self.gewonnen, signal_meldung = signalfeuer_bauen(self.spieler)
            meldung += "\n\n" + signal_meldung

        return self.aktion_abschliessen(meldung)

    def bestenliste_text(self):
        return self.bestenliste.anzeigen()
