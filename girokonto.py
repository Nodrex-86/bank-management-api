from konto import Konto

class Girokonto(Konto):
    """
    Repräsentiert ein Girokonto mit Überziehungsrahmen (Dispo).
    
    Attributes:
        inhaber (str): Name des Kontoinhabers (vererbt).
        kontostand (float): Aktueller Saldo, kann bis zum Dispo-Limit negativ sein.
        dispo (float): Maximal erlaubter Überziehungsrahmen (positiver Wert).
    """
    def __init__(self, inhaber, kontostand, dispo):
        # Initialisierung von self.dispo vor super().__init__ ist notwendig, 
        # da der überschriebene Kontostand-Setter bereits während super() 
        # auf das Attribut _dispo zugreifen muss.
        self.dispo = dispo
        super().__init__(inhaber, kontostand)
        
    @property
    def dispo(self):
        """float: Gibt den aktuellen Überziehungsrahmen zurück."""
        return self._dispo
    
    @dispo.setter
    def dispo(self, value):
        """
        Validiert das Dispo-Limit vor der Zuweisung.

        Args:
            value (float): Der festzulegende Dispo-Betrag.

        Raises:
            TypeError: Wenn der Wert keine Zahl ist.
            ValueError: Wenn der Wert negativ ist.
        """
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError("Girokonto: Der Dispo-Betrag muss eine Zahl sein.")
        if value < 0:
            raise ValueError("Girokonto: Das Dispo-Limit darf nicht negativ sein.")
        self._dispo = value

    @Konto.kontostand.setter
    def kontostand(self, value):
        """
        Überschreibt den Setter der Basisklasse, um negative Salden 
        innerhalb des Dispo-Rahmens zu ermöglichen.

        Args:
            value (float): Der neue Kontostand.

        Raises:
            TypeError: Wenn der Kontostand keine Zahl ist.
            ValueError: Wenn der Kontostand das Dispo-Limit überschreitet.
        """
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError("Girokonto: Der Kontostand muss eine Zahl sein.")
        
        # Validierung: Der Kontostand darf nicht tiefer als -dispo sinken.
        if value < -self.dispo:
            raise ValueError(f"Girokonto: Dispo-Limit von {self.dispo:.2f} EUR überschritten.")
        self._kontostand = value
    
    def abheben(self, value):
        """
        Hebt einen Betrag unter Berücksichtigung des verfügbaren Rahmens ab.

        Args:
            value (float): Abzuhebender Betrag.

        Raises:
            TypeError: Wenn der Betrag keine Zahl ist.
            ValueError: Wenn der Betrag negativ ist oder das Gesamtlimit überschreitet.
        """
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError("Girokonto (abheben): Betrag muss eine Zahl sein.")
        
        if value < 0:
            raise ValueError("Girokonto (abheben): Der Betrag muss positiv sein.")
        
        # Prüfung: Reicht der aktuelle Kontostand + Dispo für die Abhebung?
        if value > self.kontostand + self.dispo:
            verfuegbar = self.kontostand + self.dispo
            raise ValueError(f"Girokonto (abheben): Limit überschritten. Verfügbar: {verfuegbar:.2f} EUR.")
        
        self.kontostand -= value

    def __str__(self):
        """Gibt eine Zusammenfassung des Girokontos inkl. Dispo zurück."""
        return f"Girokonto: {self.inhaber} | Saldo: {self.kontostand:.2f} EUR | Dispo: {self.dispo:.2f} EUR"
    
    def __repr__(self):
        """Technische Repräsentation des Girokonto-Objekts."""
        return f"Girokonto(inhaber={self.inhaber!r}, kontostand={self.kontostand}, dispo={self.dispo})"
