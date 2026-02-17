"""
bank-management-api
Hauptmodul zur Verwaltung und Automatisierung von Bankkonten.
Nutzung von JSON-Persistenz und interaktivem Menü.
"""
from json_storage import JSONStorage
from sparkonto import Sparkonto
from girokonto import Girokonto
from logger_config import logger

# --- KONFIGURATION ---
DB_FILE = "konten.json"

# --- PERSISTENZ (JSON) ---

def initialisiere_standard_konten():
    """Erstellt eine Liste mit Standard-Konten für den Erststart."""
    return [
        Girokonto("Tom", 500, 200),
        Sparkonto("Jim", 1000, 2)
    ]

# --- LOGIK & MENÜ ---

def filtere_konten(konten_liste, suchbegriff):
    """
    Sucht alle Konten, die den Suchbegriff im Namen enthalten.
    Gibt eine Liste der Treffer zurück.

    Args:
        konten_liste (list): Eine Liste von Konto-Objekten.
        suchbegriff (str): Der Name des gesuchten Kontoinhabers.

    Returns:
        Gibt die Liste der Treffer zurück.
    """
    begriff_bereinigt = suchbegriff.strip().lower()
    return [k for k in konten_liste if begriff_bereinigt in k.inhaber.lower()]

def interaktives_menue(konten_liste):
    """Startet die Benutzerschnittstelle für die Kontoverwaltung."""
    while True:
        print("\n--- 🏦 BANK-MANAGEMENT-SYSTEM (JSON) ---")
        print("1. Kontenübersicht anzeigen")
        print("2. Einzahlen")
        print("3. Abheben")
        print("4. Konto suchen") 
        print("5. Neues Konto erstellen")
        print("6. Zinsen gutschreiben (Kontostand ändert sich)") 
        print("7. Zinsen simulieren (Nur Testrechnung)")
        print("8. Speichern & Beenden")

        wahl = input("\nWählen Sie eine Option (1-8): ")

        if wahl == "1":
            if not konten_liste:
                print("\nKeine Konten vorhanden.")
            else:
                print("\nAktuelle Konten:")
                for k in konten_liste:
                    print(k)
        
        elif wahl == "2":
            k = None
            while True:
                name = input("Name des Inhabers (oder 'x' zum Abbrechen): ").strip()
                if name.lower() == 'x':
                    break
                try:
                    k = storage.konto_holen(name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    betrag = float(input(f"Betrag für {k.inhaber} einzahlen: "))   
                    ergebnis = k.einzahlen(betrag)    

                    storage.speichern(konten)        
                    print(f"✅  {ergebnis}")
                except ValueError as e:
                    print(f"❌  {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")

        elif wahl == "3":
            k = None
            while True:
                name = input("Name des Inhabers (oder 'x' zum Abbrechen): ").strip()
                if name.lower() == 'x':
                    break
                try:
                    k = storage.konto_holen(name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    betrag = float(input(f"Betrag von {k.inhaber} abheben: "))
                    print(f"✅  {k.abheben(betrag)}")
                except ValueError as e:
                    print(f"❌  {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")
        
        elif wahl == "4":
            begriff = input("\n🔍 Filtern nach Name: ")
            treffer = filtere_konten(konten, begriff) # Logik aufrufen
            
            if not treffer:
                print(f"⚠️  Keine Konten gefunden für: '{begriff}'")
            else:
                print(f"\n✅  {len(treffer)} Treffer gefunden:")
                for k in treffer:
                    print(k)

        elif wahl == "5":
            while True:
                name = input("Name des Inhabers (oder 'x' zum Abbrechen): ").strip()
                if name.lower() == 'x':
                    break
                # Name-Check: Existiert der Name schon?
                if storage.name_existiert(name):
                    vorschlaege = storage.generiere_vorschlaege(name)
                    print(f"❌ Name '{name}' belegt. Vorschläge: {', '.join(vorschlaege)}")
                    continue # Nochmal nach Name fragen

                while True:
                    typ = input("Typ (Giro / Spar): ").strip().lower()
                    if typ in ["giro", "spar"]:
                        break  # Korrekte Eingabe, Schleife verlassen
                    print("❌  Fehler: Bitte nur 'Giro' oder 'Spar' eingeben.")
                try:
                    start_saldo = float(input("Startguthaben: "))
                    if typ == "giro":
                        dispo = float(input("Dispo-Limit: "))
                        neues_k = Girokonto(name, start_saldo, dispo)
                    else:
                        zins = float(input("Zinssatz (%): "))
                        neues_k = Sparkonto(name, start_saldo, zins)
                    storage.konto_hinzufuegen(neues_k)
                    konten_liste.append(neues_k)
                    print(f"✅  Konto für {name} erfolgreich angelegt!")
                except ValueError as e:
                    print(f"❌ {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")
                break

        elif wahl == "6":
            k = None
            while True:
                name = input("Name des Inhabers (oder 'x' zum Abbrechen): ").strip()
                if name.lower() == 'x':
                    break
                try:
                    k = storage.konto_holen(name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    if hasattr(k, 'zinsen_berechnen'):                    
                        print(f"✅  {k.zinsen_berechnen()}")
                    else:
                        print(f"⚠️   Achtung: Konto '{name}' ist kein Sparkonto.")
                except ValueError as e:
                    print(f"❌  {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")

        elif wahl == "7":
            k = None
            while True:
                name = input("Name des Inhabers (oder 'x' zum Abbrechen): ").strip()
                if name.lower() == 'x':
                    break
                try:
                    k = storage.konto_holen(name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    if hasattr(k, 'zinsen_berechnen_mit'):
                        zins = float(input("Geben Sie den Zinssatz für die Berechnung ein: "))
                        print(f"✅ {k.zinsen_berechnen_mit(zins)}")
                    else:
                        print(f"⚠️  Sonderzins für '{name}' nicht verfügbar.")
                except ValueError as e:
                    print(f"❌ {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")

        elif wahl == "8":
            try:
                storage.speichern(konten_liste)
                print(f"✅  Daten erfolgreich in '{DB_FILE}' gesichert. Auf Wiedersehen!")
            except Exception as e:
                print(f"❌  Kritischer Fehler beim Beenden: {e}")
            break
        else:
            print("⚠️  Ungültige Eingabe, bitte versuchen Sie es erneut.")


# --- HAUPTPROGRAMM ---
if __name__ == "__main__":
    logger.info(f"Programm gestartet")
    storage = JSONStorage("konten.json")

    try:
        konten = storage.laden()

        if not konten:
            print("💡 INFO: Keine Datenbank gefunden. Standard-Konten werden angelegt.")
            konten = initialisiere_standard_konten()
            storage.speichern(konten)
            print(f"✅  Standard-Konten erfolgreich gesichert.")
        else:
            print(f"✅ INFO: {len(konten)} Konten geladen.")
    
    except Exception as e:
        print(f"❌ Kritischer Fehler beim Beenden: {e}")
        exit()

    interaktives_menue(konten)