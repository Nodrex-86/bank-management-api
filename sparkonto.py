from konto import Konto

class Sparkonto(Konto):
    """
    Repräsentiert ein Sparkonto mit Verzinsungsfunktion.

    Attributes:
        inhaber (str): Name des Kontoinhabers (vererbt).
        kontostand (float): Aktueller Saldo (darf nicht negativ sein).
        zins (float): Zinssatz in Prozent (positiver Wert).
    """
    def __init__(self, inhaber, kontostand, zins):
        super().__init__(inhaber, kontostand)
        self.zins = zins

    @property
    def zins(self):
        """float: Gibt den aktuellen Zinssatz zurück."""
        return self._zins

    @zins.setter
    def zins(self, value):
        """
        Validiert den Zinssatz vor der Zuweisung.

        Args:
            value (float): Der festzulegende Prozentsatz.

        Raises:
            TypeError: Wenn der Wert keine Zahl ist.
            ValueError: Wenn der Wert negativ ist.
        """
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError("Sparkonto: Der Zins muss eine Zahl sein.")
        if value < 0:
            raise ValueError("Sparkonto: Der Zinssatz darf nicht negativ sein.")
        self._zins = value

    def zinsen_berechnen(self):
        """
        Berechnet die Zinsen basierend auf dem aktuellen Stand und kapitalisiert diese.

        Returns:
            str: Eine Bestätigung über die Zinsgutschrift und den neuen Saldo.
        """
        factor = 1 + (self.zins / 100)
        self.kontostand *= factor
        return f"{self.zins}% Zinsen hinzugefügt. Neuer Stand: {self.kontostand:.2f} EUR"

    def zinsen_berechnen_mit(self, neuer_zins):
        """
        Berechnet die Zinsen temporär mit einem abweichenden Zinssatz.

        Args:
            neuer_zins (float): Temporärer Zinssatz in Prozent.

        Returns:
            str: Bestätigung der Berechnung mit dem neuen Zinssatz.
        """
        alter_zins = self.zins  # Speichert den ursprünglichen Zins zwischen
        try:
            self.zins = neuer_zins  # Validierung erfolgt automatisch durch den Setter
            # Wir fangen den Rückgabestring der Methode ab
            result_msg = self.zinsen_berechnen()
            return f"Berechnung mit Sonderzins ({neuer_zins}%): {result_msg}"
        finally:
            self.zins = alter_zins  # Stellt den Original-Zins sicher wieder her

    def __str__(self):
        """Benutzerfreundliche Darstellung des Sparkontos."""
        return f"Sparkonto: {self.inhaber} | Saldo: {self.kontostand:.2f} EUR | Zins: {self.zins:.2f}%"
    
    def __repr__(self):
        """Technische Objektrepräsentation."""
        return f"Sparkonto(inhaber={self.inhaber!r}, kontostand={self.kontostand}, zins={self.zins})"
