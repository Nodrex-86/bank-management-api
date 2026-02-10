"""
bank-management-api
Hauptmodul zur Verwaltung und Automatisierung von Bankkonten.
Nutzung von JSON-Persistenz.
"""
import os
import json
from sparkonto import Sparkonto
from girokonto import Girokonto

# --- KONFIGURATION ---
DB_FILE = "konten.json"

# --- PERSISTENZ (JSON) ---

def speichere_konten_json(konten_liste, dateiname=DB_FILE):
    """Speichert die Konten-Liste als strukturierte JSON-Datei."""
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
    """Lädt Konten aus einer JSON-Datei und erstellt die entsprechenden Objekte."""
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

def einzahlung_simulation(konten_liste, name, betrag):
    """
    Simuliert eine Einzahlung basierend auf dem Namen, unabhängig vom Kontotyp.

    Args:
        konten_liste (list): Die Liste der verfügbaren Konten.
        name (str): Kundenname.
        betrag (float): Betrag für die Einzahlung.
    """
    k = finde_konto(konten_liste, name)
    if k:
        try:
            alte_kontostand = k.kontostand
            k.einzahlen(betrag)
            print(f"✅ Erfolg! Alter Stand: {alte_kontostand} -> Neuer Stand: {k.kontostand:.2f} EUR")
            speichere_konten_json(konten_liste)
        except Exception as e:
            print(f"⚠️ Fehler: {e}")
    else:
        print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

def abhebung_simulation(konten_liste, name, betrag):
    """
    Simuliert eine Abhebung basierend auf dem Namen, unabhängig vom Kontotyp.

    Args:
        konten_liste (list): Die Liste der verfügbaren Konten.
        name (str): Name des Kunden.
        betrag (float): Betrag für die Abhebung.
    """
    k = finde_konto(konten_liste, name)
    if k:
        try:
            alte_kontostand = k.kontostand
            k.abheben(betrag)
            print(f"✅ Erfolg! Alter Stand: {alte_kontostand} -> Neuer Stand: {k.kontostand:.2f} EUR")
            speichere_konten_json(konten_liste)
        except Exception as e:
            print(f"⚠️ Fehler: {e}")
    else:
        print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

def zinsen_berechnung(konten_liste, name):
    """
    Berechnet den neuen Kontostand anhand des vordefinierten Zinssatzes.

    Args:
        konten_liste (list): Die Liste der verfügbaren Konten.
        name (str): Name des Kunden.
    """
    k = finde_konto(konten_liste, name)
    if k:
        try:
            alte_kontostand = k.kontostand
            if hasattr(k, 'zinsen_berechnen'):
                k.zinsen_berechnen()
                print(f"✅ Erfolg! Alter Stand: {alte_kontostand} -> Neuer Stand: {k.kontostand:.2f} EUR")
                speichere_konten_json(konten_liste)
            else:
                print(f"⚠️  Achtung: Konto '{name}' hat kein Sparkonto.")
        except Exception as e:
            print(f"⚠️ Fehler: {e}")
    else:
        print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")

def sonderzins_simulation(konten_liste, name, sonderzins):
    """Demonstriert die Berechnung mit einem temporären Sonderzinssatz."""
    k = finde_konto(konten_liste, name)
    if k and hasattr(k, 'zinsen_berechnen_mit'):
        print(f"✅ Erfolg! {k.zinsen_berechnen_mit(sonderzins)}")
        speichere_konten_json(konten_liste)
    else:
        print(f"⚠️ Sonderzins für '{name}' nicht verfügbar.")


# --- HAUPTPROGRAMM ---
if __name__ == "__main__":
    konten = lade_konten_json()

    # Falls die Liste leer ist (erster Start), erstelle Standard-Konten
    if not konten:
        print("INFO: Keine Daten gefunden. Erstelle Standard-Konten...")
        konten.append(Girokonto("Tom", 500, 200))
        konten.append(Sparkonto("Jim", 1000, 2))
        # Optional: Sofort speichern, damit die Datei existiert
        speichere_konten_json(konten)
    einzahlung_simulation(konten, "Tom", 100)
    abhebung_simulation(konten, "Jim", 100)
    zinsen_berechnung(konten, "Tom")
    zinsen_berechnung(konten, "Jim")
    sonderzins_simulation(konten, "Jim", 5)