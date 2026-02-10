"""
bank-management-api
Hauptmodul zur Verwaltung und Automatisierung von Bankkonten.
Nutzung von JSON-Persistenz und interaktivem Menü.
"""
import os
import json
from sparkonto import Sparkonto
from girokonto import Girokonto

# --- KONFIGURATION ---
DB_FILE = "konten.json"

# --- PERSISTENZ (JSON) ---

def speichere_konten_json(konten_liste, dateiname=DB_FILE):
    """
    Speichert die Konten-Liste als strukturierte JSON-Datei.

    Args:
        konten_liste (list): Liste der Konto-Objekte.
        dateiname (str): Name der Zieldatei.
    """
    daten = []
    for k in konten_liste:
        # Erstellung eines Dictionaries für die JSON-Struktur
        konto_dict = {
            "inhaber": k.inhaber,
            "kontostand": k.kontostand,
            "typ": type(k).__name__,
            "extra": k.dispo if isinstance(k, Girokonto) else k.zins
        }
        daten.append(konto_dict)
    
    try:
        with open(dateiname, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4)
        print(f"✅ INFO: Daten in '{dateiname}' gesichert.")
    except Exception as e:
        print(f"❌ FEHLER beim Speichern: {e}")

def lade_konten_json(dateiname=DB_FILE):
    """
    Lädt Konten aus einer JSON-Datei und erstellt die entsprechenden Objekte.

    Args:
        dateiname (str): Name der Quelldatei.

    Returns:
        list: Eine Liste mit instanziierten Girokonto- und Sparkonto-Objekten.
    """
    geladene_konten = []
    if not os.path.exists(dateiname):
        print(f"✅ INFO: Keine Bestandsdatei '{dateiname}' gefunden. Starte leer.")
        return geladene_konten
    
    try:
        with open(dateiname, "r", encoding="utf-8") as f:
            daten = json.load(f)
            for d in daten:
                if d["typ"] == "Girokonto":
                    k = Girokonto(d["inhaber"], d["kontostand"], d["extra"])
                elif d["typ"] == "Sparkonto":
                    k = Sparkonto(d["inhaber"], d["kontostand"], d["extra"])
                geladene_konten.append(k)
        print(f"✅ INFO: {len(geladene_konten)} Konten erfolgreich aus JSON geladen.")
    except Exception as e:
        print(f"❌ FEHLER beim Laden der JSON-Daten: {e}")
    
    return geladene_konten

# --- LOGIK & MENÜ ---

def finde_konto(konten_liste, name):
    """
    Sucht ein Konto in der Liste basierend auf dem Inhabernamen.
    
    Die Suche ist case-insensitive (ignoriert Groß-/Kleinschreibung) 
    und entfernt führende oder nachfolgende Leerzeichen im Suchbegriff.

    Args:
        konten_liste (list): Eine Liste von Konto-Objekten.
        name (str): Der Name des gesuchten Kontoinhabers.

    Returns:
        object: Das gefundene Konto-Objekt oder None, wenn kein Treffer erzielt wurde.
    """
    return next((k for k in konten_liste if k.inhaber.lower() == name.strip().lower()), None)

def interaktives_menue(konten_liste):
    """Startet die Benutzerschnittstelle für die Kontoverwaltung."""
    while True:
        print("\n--- 🏦 BANK-MANAGEMENT-SYSTEM (JSON) ---")
        print("1. Kontenübersicht anzeigen")
        print("2. Einzahlen")
        print("3. Abheben")
        print("4. Neues Konto erstellen")
        print("5. Zinsen gutschreiben (Kontostand ändert sich)") 
        print("6. Zinsen simulieren (Nur Testrechnung)")
        print("7. Speichern & Beenden")

        wahl = input("\nWählen Sie eine Option (1-7): ")

        if wahl == "1":
            if not konten_liste:
                print("\nKeine Konten vorhanden.")
            else:
                print("\nAktuelle Konten:")
                for k in konten_liste:
                    print(k)
        
        elif wahl == "2":
            name = input("Name des Inhabers: ")
            k = finde_konto(konten_liste, name)
            if k:
                try:
                    betrag = float(input(f"Betrag für {k.inhaber} einzahlen: "))               
                    print(f"✅  {k.einzahlen(betrag)}")
                except Exception as e:
                    print(f"⚠️ Fehler: {e}")
            else:
                print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

        elif wahl == "3":
            name = input("Name des Inhabers: ")
            k = finde_konto(konten_liste, name)
            if k:
                try:
                    betrag = float(input(f"Betrag von {k.inhaber} abheben: "))
                    print(f"✅ {k.abheben(betrag)}")
                except Exception as e:
                    print(f"⚠️ Fehler: {e}")
            else:
                print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

        elif wahl == "4":
            name = input("Name des Inhabers: ")
            typ = input("Typ (Giro / Spar): ").strip().lower()
            try:
                start_saldo = float(input("Startguthaben: "))
                if typ == "giro":
                    dispo = float(input("Dispo-Limit: "))
                    neues_k = Girokonto(name, start_saldo, dispo)
                elif typ == "spar":
                    zins = float(input("Zinssatz (%): "))
                    neues_k = Sparkonto(name, start_saldo, zins)
                else:
                    print("❌ Fehler: Ungültiger Kontotyp! Bitte 'Giro' oder 'Spar' eingeben.")
                    continue # Springt zurück zum Menüanfang
                
                konten_liste.append(neues_k)
                print(f"✅ Konto für {name} erfolgreich angelegt!")
            except Exception as e:
                print(f"⚠️ Fehler beim Erstellen: {e}")

        elif wahl == "5":
            name = input("Name des Inhabers für Zinsgutschrift: ")
            k = finde_konto(konten_liste, name)
            if k:
                try:
                    if hasattr(k, 'zinsen_berechnen'):                    
                        print(f"✅ {k.zinsen_berechnen()}")
                    else:
                        print(f"⚠️  Achtung: Konto '{name}' ist kein Sparkonto.")
                except Exception as e:
                    print(f"⚠️ Fehler: {e}")
            else:
                print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

        elif wahl == "6":
            name = input("Name des Inhabers: ")
            k = finde_konto(konten_liste, name)
            if k:
                try:
                    if hasattr(k, 'zinsen_berechnen_mit'):
                        zins = float(input("Geben Sie den Zinssatz für die Berechnung ein: "))
                        print(f"✅ {k.zinsen_berechnen_mit(zins)}")
                    else:
                        print(f"⚠️ Sonderzins für '{name}' nicht verfügbar.")
                except Exception as e:
                    print(f"⚠️ Fehler: {e}")
            else:
                print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

        elif wahl == "7":
            speichere_konten_json(konten_liste)
            print("✅ Daten gespeichert. Auf Wiedersehen!")
            break
        else:
            print("⚠️ Ungültige Eingabe, bitte versuchen Sie es erneut.")


# --- HAUPTPROGRAMM ---
if __name__ == "__main__":
    konten = lade_konten_json()

    # Falls die Liste leer ist (erster Start), erstelle Standard-Konten
    if not konten:
        print("INFO: Keine Daten gefunden. Erstelle Standard-Konten...")
        konten.append(Girokonto("Tom", 500, 200))
        konten.append(Sparkonto("Jim", 1000, 2))
        speichere_konten_json(konten)

    interaktives_menue(konten)