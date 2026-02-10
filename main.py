"""
bank-management-api
Hauptmodul zur Verwaltung und Automatisierung von Bankkonten.
"""


from sparkonto import Sparkonto
from girokonto import Girokonto

konten = []
konten.append(Girokonto("Tom", 500, 200))
konten.append(Sparkonto("Jim", 1000, 2))

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
            else:
                print(f"⚠️  Achtung: Konto '{name}' hat kein Sparkonto.")
        except Exception as e:
            print(f"⚠️ Fehler: {e}")
    else:
        print(f"❌ Fehler: Konto für '{name}' nicht gefunden.")


einzahlung_simulation(konten, "Tom", 100)
abhebung_simulation(konten, "Jim", 100)
zinsen_berechnung(konten, "Tom")
zinsen_berechnung(konten, "Jim")