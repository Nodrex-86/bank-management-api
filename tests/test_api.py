import unittest
from fastapi.testclient import TestClient
from api import app

class TestBankAPI(unittest.TestCase):
    def setUp(self):
        from api import stelle_datenbank_sicher
        stelle_datenbank_sicher()
        self.client = TestClient(app)

    # --- TAG: Allgemein ---
    def test_home(self):
        """
        Testet den Willkommens-Endounkt
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    # --- TAG: 1. Übersicht ---
    def test_alle_konten(self):
        """
        Prüft, ob die Konktenliste (Array) zurückgegeben wird.
        """
        response = self.client.get("/konten")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # --- TAG: 2. Transaktionen ---
    def test_einzahlen_erfolgreich(self):
        """
        Testen Erfolgreiche Einzahlung
        """
        response = self.client.post("/transaktion/einzahlen/Tom?betrag=100")
        self.assertEqual(response.status_code, 200)
        self.assertIn("eingezahlt", response.json()["nachricht"].lower())

    def test_abheben_error(self):
        """
        Testet Fehler bei zu hohen Betrag
        """
        response = self.client.post("/transaktion/abheben/Tom?betrag=100000")
        self.assertEqual(response.status_code, 400)

    

    # --- TAG: 3. Verwaltung ---
    def test_suche_ergebnis(self):
        """
        Testet die Suchfunktion mit einem bekannten Namen (z.B. Tom).
        """
        # 'Tom' sollte in Datenbank existieren
        response = self.client.get("/suche?name=Tom")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if isinstance(data, list):
            self.assertTrue(any("Tom" in k["inhaber"] for k in data))
    
    def test_konto_erstellen(self):
        payload = {
            "name":"NodRex",
            "typ": "giro",
            "start_saldo": 1000,
            "extra": 200
        }
        response = self.client.post("/konten/erstellen", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_konto_erstellen_error(self):
        """
        Testet, ob ungültige Kontotypen angelehnt werden (400 Bad Request).
        """
        payload = {
            "name": "TestUser",
            "typ": "falscher_typ",
            "start_saldo": 100,
            "extra": 0
        }
        response = self.client.post("/konten/erstellen", json=payload)
        self.assertEqual(response.status_code, 400)

    # --- TAG: 4. Zinsen ---
    def test_zinsen_gutschreiben(self):
        """
        Testet, ob auf Sparkonto Zinsen richtig gutgeschrieben wird
        """
        response = self.client.post("/zinsen/gutschreiben/Jim")
        if response.status_code == 200:
            self.assertIn("Erfolg", response.json()["status"])
        else:
            self.assertEqual(response.status_code, 400)
    

    def test_zinsen_simulation_spar(self):
        """
        testet, Zinsem Simulation mit 'jim' (Sparkonto)
        """
        response = self.client.post("/zinsen/simulieren/Jim?sonderzins=5.0")
        if response.status_code == 200:
            self.assertIn("Simulation", response.json()["status"])
        else:
            self.assertEqual(response.status_code, 400)


    def test_zinsen_simulation_error(self):
        """
        Prüft, ob Simulation bei ungültigen Werten (z.B. Zins <= 0) blokiert
        """
        response = self.client.post("/zinsen/simulieren/Tom?sonderzins=-5.0")
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()