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
    def zins(self, betrag):
        """
        Validiert den Zinssatz vor der Zuweisung.

        Args:
            betrag (float): Der festzulegende Prozentsatz.

        Raises:
            TypeError: Wenn der Wert keine Zahl ist.
            ValueError: Wenn der Wert negativ ist.
        """
        try:
            betrag = float(betrag)
        except (ValueError, TypeError):
            raise TypeError("Sparkonto: Der Zins muss eine Zahl sein.")
        if betrag < 0:
            raise ValueError("Sparkonto: Der Zinssatz darf nicht negativ sein.")
        self._zins = betrag

    def zinsen_berechnen(self):
        """
        Berechnet die Zinsen basierend auf dem Zinssatz und aktualisiert den Saldo.

        Returns:
            str: Eine Bestätigung über die Zinsberechnung und das Ergebnis.
        """
        factor = 1 + (self.zins / 100)
        self.kontostand *= factor
        return f"Zinsberechnung mit {self.zins}% erfolgt. Stand: {self.kontostand:.2f} EUR"
    

    def zinsen_berechnen_mit(self, neuer_zins):
        """
        Simuliert die Zinsberechnung temporär mit einem abweichenden Zinssatz, 
        ohne den Kontostand dauerhaft zu verändern.

        Args:
            neuer_zins (float): Der zu simulierende Zinssatz in Prozent.

        Returns:
            str: Eine Nachricht mit dem Ergebnis der Simulation.
        """
        # Werte zwischenspeichern, um sie später wiederherzustellen
        alter_kontostand = self.kontostand  
        alter_zins = self.zins  
        
        try:
            self.zins = neuer_zins  
            # Führt die Berechnung aus und speichert die Nachricht
            result_msg = self.zinsen_berechnen()
            return f"Simulation erfolgreich: {result_msg}"
        finally:
            # Stellt den Original-Zustand des Objekts wieder her
            self.zins = alter_zins  
            self.kontostand = alter_kontostand


    def __str__(self):
        """Benutzerfreundliche Darstellung des Sparkontos."""
        return f"Sparkonto: {self.inhaber} | Saldo: {self.kontostand:.2f} EUR | Zins: {self.zins:.2f}%"
    
    def __repr__(self):
        """Technische Objektrepräsentation."""
        return f"Sparkonto(inhaber={self.inhaber!r}, kontostand={self.kontostand}, zins={self.zins})"
