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

    Raises:
        IOError: Wenn die Datei nicht geschrieben werden kann.
    """
    daten = []
    for k in konten_liste:
        # Erstellung eines Dictionaries für die JSON-Struktur
        konto_dict = {
            "inhaber": k.inhaber,
            "kontostand": k.kontostand,
            "typ": type(k).__name__,
            "extra": getattr(k, 'dispo', getattr(k, 'zins', None))
        }
        daten.append(konto_dict)
    
    try:
        with open(dateiname, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4)
    except Exception as e:
        raise IOError(f"❌ Speichervorgang fehlgeschlagen: {e}")

def lade_konten_json(dateiname=DB_FILE):
    """
    Lädt Konten aus einer JSON-Datei.
    
    Returns:
        list: Liste der Konten (leer, falls Datei nicht existiert).

    Raises:
        RuntimeError: Wenn die Datei beschädigt ist.
    """
    if not os.path.exists(dateiname):
        return []
    
    geladene_konten = []
    try:
        with open(dateiname, "r", encoding="utf-8") as f:
            daten = json.load(f)
            for d in daten:
                if d["typ"] == "Girokonto":
                    k = Girokonto(d["inhaber"], d["kontostand"], d["extra"])
                elif d["typ"] == "Sparkonto":
                    k = Sparkonto(d["inhaber"], d["kontostand"], d["extra"])
                geladene_konten.append(k)
        return geladene_konten
    except Exception as e:
        raise RuntimeError(f" Datenbankfehler: {e}")
    
    return geladene_konten

def initialisiere_standard_konten():
    """Erstellt eine Liste mit Standard-Konten für den Erststart."""
    return [
        Girokonto("Tom", 500, 200),
        Sparkonto("Jim", 1000, 2)
    ]

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
        object: Das gefundene Konto-Objekt.
    
    Raises:
        ValueError: Wenn Konto-Objekt ist None und kein Treffer erzielt wurde.
    """
    name_bereinigt = name.strip().lower()
    konto = next((k for k in konten_liste if k.inhaber.lower() == name_bereinigt), None)
    if konto is None:
        raise ValueError(f"Konto für '{name}' wurde nicht gefunden.")
    
    return konto

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
                name = input("Name des Inhabers: ")
                if name.lower() == 'x':
                    break
                try:
                    k = finde_konto(konten_liste, name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    k = finde_konto(konten_liste, name)
                    betrag = float(input(f"Betrag für {k.inhaber} einzahlen: "))               
                    print(f"✅  {k.einzahlen(betrag)}")
                except ValueError as e:
                    print(f"❌  {e}")
                except Exception as e:
                    print(f"⚠️  Unerwarteter Fehler: {e}")

        elif wahl == "3":
            k = None
            while True:
                name = input("Name des Inhabers: ")
                if name.lower() == 'x':
                    break
                try:
                    k = finde_konto(konten_liste, name)
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
            name = input("Name des Inhabers: ")

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
                
                konten_liste.append(neues_k)
                print(f"✅  Konto für {name} erfolgreich angelegt!")
            except ValueError as e:
                # Fängt sowohl falsche Zahlen als auch den ungültigen Typ ab
                print(f"❌  Eingabefehler: {e}")
            except Exception as e:
                print(f"⚠️  Unerwarteter Fehler: {e}")

        elif wahl == "6":
            k = None
            while True:
                name = input("Name des Inhabers für Zinsgutschrift: ")
                if name.lower() == 'x':
                    break
                try:
                    k = finde_konto(konten_liste, name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    k = finde_konto(konten_liste, name)
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
                name = input("Name des Inhabers: ")
                if name.lower() == 'x':
                    break
                try:
                    k = finde_konto(konten_liste, name)
                    break
                except ValueError:
                    print(f"⚠️  Konto für '{name}' nicht gefunden. Bitte versuchen Sie es erneut(oder 'x' zum Abbrechen).")
            if k:
                try:
                    k = finde_konto(konten_liste, name)
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
                speichere_konten_json(konten_liste)
                print(f"✅  Daten erfolgreich in '{DB_FILE}' gesichert. Auf Wiedersehen!")
            except Exception as e:
                print(f"❌  Kritischer Fehler beim Beenden: {e}")
            break
        else:
            print("⚠️  Ungültige Eingabe, bitte versuchen Sie es erneut.")


# --- HAUPTPROGRAMM ---
if __name__ == "__main__":
    try:
        konten = lade_konten_json()
        # Falls die Liste leer ist (erster Start), erstelle Standard-Konten
        if not konten:
            print("💡 INFO: Keine Datenbank gefunden. Standard-Konten werden angelegt.")
            konten = initialisiere_standard_konten()
            try:
                speichere_konten_json(konten)
                print(f"✅ Standard-Konten erfolgreich in '{DB_FILE}' gesichert")
            except Exception as e:
                print(f"❌ Kritischer Fehler beim Beenden: {e}")
        else:
            print(f"✅ INFO: {len(konten)} Konten erfolgreich aus JSON geladen.")
    except RuntimeError as e:
        print(f"❌ KRITISCHER FEHLER: {e}")
        print("Das Programm wird beendet.")
        exit()

    interaktives_menue(konten)