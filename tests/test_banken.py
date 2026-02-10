import unittest
from girokonto import Girokonto
from sparkonto import Sparkonto

class TestGirokonto(unittest.TestCase):
    """
    Test-Suite für die Validierung der Girokonto-Logik.
    Prüft Dispo-Grenzen, Initialisierung und Fehlerbehandlung.
    """
    def setUp(self):
        self.giro = Girokonto("Tom", 500.0, 200.0)

    def test_giro_initialisierung_erfolgreich_negativ(self):
        """Prüft, ob ein Girokonto direkt im Minus (innerhalb Dispo) erstellt werden kann."""
        # Start mit -100 bei 200 Dispo -> Sollte klappen
        test_giro = Girokonto("Max", -100, 200)
        self.assertEqual(test_giro.kontostand, -100)

    def test_giro_initialisierung_ausserhalb_dispo_fail(self):
        """Prüft, ob ein Girokonto mit Startwert unter dem Dispo-limit blokiert wird."""
        # Start mit -300 bei nur 200 Dispo -> Muss Fehler werfen
        with self.assertRaises(ValueError):
            Girokonto("Moritz", -300, 200)
    
    def test_giro_initialisierung_dispo_negativ_fail(self):
        """Prüft, ob ein negativer Dispo-Rahmen bei Erstellung abgelehnt wird."""
        with self.assertRaises(ValueError):
            Girokonto("Susi", 500, -50)
    
    def test_giro_initialisierung_dispo_string_fail(self):
        """Prüft, ob ein String im Dispo blokiert wird"""
        with self.assertRaises(TypeError):
            Girokonto("Susi", 200, "Hundert Euro")

    def test_abheben_string_fail(self):
        """Prüft, ob das System bei einem String statt einer Zahl blockiert."""
        with self.assertRaises(TypeError):
            self.giro.abheben("Hundert Euro") # Das muss einen Fehler werfen!

    def test_dispo_limit(self):
        """Prüft, ob das Abheben innerhalb des Dispos funktioniert."""
        self.giro.abheben(650) # 500 Guthaben + 150 Dispo
        self.assertEqual(self.giro.kontostand, -150.0)

    def test_dispo_ueberschritten(self):
        """Prüft, ob das Limit (Guthaben + Dispo) streng eingehalten wird."""
        with self.assertRaises(ValueError):
            self.giro.abheben(701) # 500 + 200 = 700 Limit

class TestSparkonto(unittest.TestCase):
    """
    Test-Suite für die Validierung der Sparkonto-Logik.
    Prüft Zinsen, Initialisierung und Fehlerbehandlung.
    """
    def setUp(self):
        self.spar = Sparkonto("Jim", 1000.0, 2.0)

    def test_spar_initialisierung_zins_string_fail(self):
        """Prüft, ob ein String im zins blokiert wird"""
        with self.assertRaises(TypeError):
            Sparkonto("Susi", 200, "Hundert Euro")

    def test_spar_initialisierung_zins_negativ_fail(self):
        """Prüft, ob negative Zahl im zins blokiert wird"""
        with self.assertRaises(ValueError):
            Sparkonto("Susi", 200, -10)

    def test_zinsen_kapitalisierung(self):
        """Prüft, ob 2% Zinsen auf 1000€ korrekt 1020€ ergeben."""
        self.spar.zinsen_berechnen()
        self.assertEqual(self.spar.kontostand, 1020.0)

if __name__ == "__main__":
    unittest.main()
