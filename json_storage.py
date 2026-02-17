import json
import os
from storage_interface import StorageInterface
from sparkonto import Sparkonto
from girokonto import Girokonto
import random
from logger_config import logger



class JSONStorage(StorageInterface):
    """
    Implementierung einer JSON-basierten Speicherung für Bankkonten.
    """
    def __init__(self, dateiname="konten.json"):
        """
        Initialisiert den JSON-Speicher.

        Args:
            dateiname (str): Der Name der JSON-Datei. Standard ist 'konten.json'.
        """
        self.dateiname = dateiname

    def laden(self):
        """
        Lädt Konten aus einer JSON-Datei und erstellt die entsprechenden Objekte.

        Returns:
            list: Liste der geladenen Konto-Objekte.

        Raises:
            RuntimeError: Wenn die JSON-Datei beschädigt ist oder nicht gelesen werden kann.
        """
        if not os.path.exists(self.dateiname):
            return []
        
        geladene_konten = []
        try:
            with open(self.dateiname, "r", encoding="utf-8") as f:
                daten = json.load(f)
                for d in daten:
                    if d["typ"] == "Girokonto":
                        k = Girokonto(d["inhaber"], d["kontostand"], d["extra"])
                    elif d["typ"] == "Sparkonto":
                        k = Sparkonto(d["inhaber"], d["kontostand"], d["extra"])
                    geladene_konten.append(k)
            logger.info(f"JSON-Daten erfolgreich geladen ({self.dateiname})")
            return geladene_konten
        except Exception as e:
            logger.error(f"Datenbankfehler (JSON) bein Laden von {self.dateiname}: {e}")
            raise RuntimeError(f"Datenbankfehler (JSON): {e}")
        
    def speichern(self, konten_liste):
        """
        Serialisiert die Konten-Liste in eine JSON-Datei.

        Args:
            konten_liste (list): Liste der Girokonto- oder Sparkonto-Objekte.

        Raises:
            IOError: Wenn die Datei nicht geschrieben werden kann.
        """
        daten = []
        for k in konten_liste:
            daten.append({
                "inhaber": k.inhaber,
                "kontostand": k.kontostand,
                "typ": type(k).__name__,
                "extra": getattr(k, 'dispo', getattr(k, 'zins', None))
            })
        try:
            with open(self.dateiname, "w", encoding="utf-8") as f:
                json.dump(daten, f, indent=4)
            logger.info(f"Speichervorgang (JSON) erfolgreich in {self.dateiname} gesichert")
        except Exception as e:
            logger.error(f"Speichervorgang (JSON) fehlergeschlagen ({self.dateiname}): {e}")
            raise IOError(f"Speichervorgang (JSON) fehlergeschlagen : {e}")
        
    def name_existiert(self, name):
        """
        Name-Check für Konto

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.

        Returns:
            bool: Gibt True zurück, wenn der Name (case-insensitive) bereits existiert.
        """
        name_bereinigt = name.strip().lower()
        aktuelle_konten = self.laden()
        return any(k.inhaber.lower() == name_bereinigt.strip().lower() for k in aktuelle_konten)
    
    def konto_holen(self, name):
        """
        Sucht ein Konto in der Liste(JSON-Datei) basierend auf dem Inhabernamen.
    
        Die Suche ist case-insensitive (ignoriert Groß-/Kleinschreibung) 
        und entfernt führende oder nachfolgende Leerzeichen im Suchbegriff.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.

        Raises:
            ValueError: Wenn Konto-Objekt ist None und kein Treffer erzielt wurde.

        Returns:
            object: Das gefundene Konto-Objekt.
        """
        name_bereinigt = name.strip().lower()
        konten = self.laden() # Lädt aktuelle Daten
        konto = next((k for k in konten if k.inhaber.lower() == name_bereinigt), None)
        if konto is None:
            logger.warning(f"Konto für '{name}' wurde in ({self.dateiname}) nicht gefunden.")
            raise ValueError(f"Konto für '{name}' wurde in ({self.dateiname}) nicht gefunden.")
        return konto
    
    def generiere_vorschlaege(self, name):
        """
        Erzeugt 3 Namensvorschläge mit Zufallszahlen.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.

        Returns:
            Namen (list): Gibt Namen liste zurück, wenn der Name (case-insensitive) bereits existiert.
        """
        # Vorschläge generierung
        vorschlaege  = []
        aktuelle_konten = self.laden()
        while len(vorschlaege) < 3:
            nr = random.randint(10, 99)
            neuer_name = f"{name}{nr}"
            # Sicherstellen, dass der Vorschlag nich auch schon existiert
            if not any(k.inhaber.lower() == neuer_name.lower() for k in aktuelle_konten):
                if neuer_name not in vorschlaege:
                    vorschlaege.append(neuer_name)
        return vorschlaege
        
    def konto_hinzufuegen(self, konto):
        """
        Prüft auf Namensdoppelungen und fügt das Konto hinzu.
        Falls der Name existiert, wird ein Fehler mit Namensvorschlägen geworfen.
        """
        if self.name_existiert(konto.inhaber):
            vorschlaege = self.generiere_vorschlaege(konto.inhaber)
            logger.warning(f"Versuchtes Duplikat (JSON) ebgelehnt für Inhaber: {konto.inhaber}")
            raise ValueError(f"Name existiert bereits. Vorschläge: {', '.join(vorschlaege)}")
        
        aktuelle_konten = self.laden()
        aktuelle_konten.append(konto)
        logger.info(f"Neues Konto (JSON) erstellt: {konto.inhaber} ({type(konto).__name__})")
        self.speichern(aktuelle_konten)