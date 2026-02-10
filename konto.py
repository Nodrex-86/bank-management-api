class Konto: 
    """
    Repräsentiert ein Bankkonto mit Validierung des Kontostands.

    Attributes:
        inhaber (str): Name des Kontoinhabers.
        kontostand (float): Aktueller Saldo des Kontos (darf nicht negativ sein).
    """

    def __init__(self, inhaber: str, kontostand: float):
        self.inhaber = inhaber
        # Wir nutzen den Setter direkt, um Validierung beim Erstellen zu erzwingen
        self.kontostand = kontostand

    @property
    def kontostand(self):
        """float: Gibt den aktuellen Kontostand zurück."""
        return self._kontostand
    
    @kontostand.setter
    def kontostand(self, betrag):
        """
        Validiert den Betrag, bevor er im Kontostand gespeichert wird.

        Args:
            betrag (float): Der zu setzende Kontostand.

        Raises:
            TypeError: Wenn der Wert keine Zahl ist.
            ValueError: Wenn der Wert negativ ist.
        """
        try:
            betrag = float(betrag)
        except (ValueError, TypeError):
            raise TypeError("Konto: Der Betrag muss eine Zahl sein!")
        
        if betrag < 0:
            raise ValueError("Konto: Der Kontostand darf nicht negativ sein.")
        self._get_private_stand = betrag # Interner Speicherwert
        self._kontostand = betrag

    def einzahlen(self, betrag):
        """
        Erhöht den Kontostand um einen positiven Betrag.

        Args:
            betrag (float): Der einzuzahlende Betrag.

        Raises:
            TypeError: Wenn der Betrag keine Zahl ist.
            ValueError: Wenn der Betrag kleiner oder gleich 0 ist.
        """
        try:
            betrag = float(betrag)
        except (ValueError, TypeError):
            raise TypeError("Konto (einzahlen): Betrag muss eine Zahl sein!")
        
        if betrag <= 0:
            raise ValueError("Konto (einzahlen): Der Betrag muss größer als 0 sein.")
        self.kontostand += betrag
        return f"{betrag:.2f} EUR eingezahlt. Neuer Stand: {self.kontostand:.2f} EUR"

    def abheben(self, betrag):
        """
        Zieht einen Betrag vom Konto ab, sofern Deckung vorhanden ist.

        Args:
            betrag (float): Der abzuhebende Betrag.

        Raises:
            TypeError: Wenn der Betrag keine Zahl ist.
            ValueError: Wenn der Betrag <= 0 ist oder das Konto übersteigt.
        """
        try:
            betrag = float(betrag)
        except (ValueError, TypeError):
            raise TypeError("Konto (abheben): Betrag muss eine Zahl sein!")
            
        if betrag <= 0:
            raise ValueError("Konto (abheben): Betrag muss positiv sein.")
        if betrag > self.kontostand:
            raise ValueError("Konto (abheben): Betrag übersteigt den Kontostand.")
        self.kontostand -= betrag
        return f"{betrag:.2f} EUR abgehoben. Neuer Stand: {self.kontostand:.2f} EUR"

    def __str__(self):
        """Gibt eine benutzerfreundliche Zusammenfassung des Kontos zurück."""
        return f"Inhaber: {self.inhaber} | Saldo: {self.kontostand:.2f} EUR"
    
    def __repr__(self):
        """Gibt eine technische Repräsentation des Objekts zurück."""
        return f"Konto(inhaber={self.inhaber!r}, kontostand={self.kontostand})"
