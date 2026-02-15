from abc import ABC, abstractmethod

class StorageInterface(ABC):
    """
    Abstrakte Basisklasse für Speicher-Provider.
    Garantiert, dass JSON-, CSV- und SQL-Provider die gleichen Methodensignaturen nutzen.

    Args:
        ABC (ABC-Modul): (Abstract Base Class), um sicherzustellen, dass alle Unterklassen (wie JSONStorage oder SQLiteStorage) die vorgegebenen Methoden implementieren.
    """

    @abstractmethod
    def laden(self):
        """
        Lädt alle Konten asu dem Speicher.

        Returns:
            list: Eine Liste von Girokonto- und Sparkonto-Objekten.
        """
        pass

    @abstractmethod
    def speichern(self, konten_liste):
        """
        Speichert die gesamte Konten-Liste.

        Args:
            konten_liste (list): Die Liste der zu sichernden Konto-Objekte.
        """
        pass

    @abstractmethod
    def name_existiert(self,name):
        """
        Prüft, ob ein Inhabername bereits im Speicher vorhanden ist.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.
        """
        pass

    @abstractmethod
    def konto_holen(self, name):
        """
        Sucht ein einzelnes Konto anhand des Namens im Speicher.
        
        Returns:
            object: Das Konto-Objekt.
        Raises:
            ValueError: Wenn das Konto nicht existiert.
        """
        pass

    @abstractmethod
    def konto_hinzufuegen(self, konto):
        """
        Fügt ein einzelnes Konto zum Speicher hinzu. 
        (Wichtig für die SQL-Performance, um nicht die gesamte DB neu zu schreiben).

        Args:
            konto (object): Das Konto-Objekt (Giro- oder Sparkonto), das hinzugefügt werden soll.
        """
        pass