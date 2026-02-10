import unittest
from konto import Konto

class Testkonto(unittest.TestCase):
    """Test-Suite für die BasisKlasse Konto."""

    def setUp(self):
        """Initialisierung eines Testobjekts vo jedem Testfall."""
        self.test_konto = Konto("TestUser", 100)

    def test_initialisierung(self):
        """Prüft, ob Name und Kontostand korrekt gesetzt werden."""
        self.assertEqual(self.test_konto.inhaber, "TestUser")
        self.assertEqual(self.test_konto.kontostand, 100)

    def test_initialisierung_negative_zahl_fail(self):
        """Prüft, ob die Erstellung mit negativem Kontostand blokiert wird."""
        with self.assertRaises(ValueError):
            Konto("Betruger", -100)

    def test_initialisierung_string_fail(self):
        """Prüft, ob die Erstellung mit einem String als Kontostand blokiert wird."""
        with self.assertRaises(TypeError):
            Konto("Unwissender", "Tausend Euro")
            
    def test_einzahlen_erfolgreich(self):
        """Prüft, ob Einzahlung den Saldo Korrekt erhöhen."""
        self.test_konto.einzahlen(50)
        self.assertEqual(self.test_konto.kontostand, 150)

    def test_einzahlen_string_fail(self):
        """Prüft, ob das System bei einem String statt einer Zahl blockiert."""
        with self.assertRaises(TypeError):
            self.test_konto.einzahlen("Hundert Euro") # Das muss einen Fehler werfen!

    def test_einzahlen_negativ_fail(self):
        """Prüft, ob negative Einzahlungen ein ValueError auslösen."""
        with self.assertRaises(ValueError):
            self.test_konto.einzahlen(-10)

    def test_abheben_erfolgreich(self):
        """Prüft, ob Abhebungen den Saldo Korrekt verringern"""
        self.test_konto.abheben(40)
        self.assertEqual(self.test_konto.kontostand, 60)

    def test_abheben_string_fail(self):
        """Prüft, ob das System bei einem String statt einer Zahl blockiert."""
        with self.assertRaises(TypeError):
            self.test_konto.abheben("Hundert Euro") # Das muss einen Fehler werfen!

    def test_abheben_ueberdeckung_fail(self):
        """Prüft, ob Abheben über das Limit einen ValueError auslöst"""
        with self.assertRaises(ValueError):
            self.test_konto.abheben(150)

if __name__ == "__main__":
    unittest.main()