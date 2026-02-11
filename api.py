from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from main import lade_konten_json, speichere_konten_json, finde_konto
from sparkonto import Sparkonto
from girokonto import Girokonto

app = FastAPI(
    title="🏦 Nodrex Bank-Management API",
    description="Eine professionelle REST-Schnittstelle zur Verwaltung von Bankkonten, basierend auf OOP-Prinzipien",
    version="1.2.0"
)

# --- MODELLE ---
class KontoErstellenSchema(BaseModel):
    """Schema für die Erstellung eines neuen Kontos."""
    name: str
    typ: str  # "giro" oder "spar"
    start_saldo: float
    extra: float

class TransaktionErgebnis(BaseModel):
    """Rückgabe-Schema für erfolgreiche Transaktionen."""
    nachricht: str
    inhaber: str
    neuer_stand: float

# --- ENDPUNKTE (Mapping des Menüs) ---

@app.get("/", tags=["Allgemein"])
def home():
    """
    **Willkommens-Endpunkt**  
    Prüft, ob die API online und erreichbar ist.
    """
    return {"status": "online", "nachricht": "Willkommen zur Professional Bank-REST-Schnittstelle"}

@app.get("/konten", tags=["1. Übersicht"])
def alle_konten():
    """
    **Alle Konten auflisten**  
    Gibt alle Konten dynamisch mit all ihren Attributen (inkl. Dispo/Zins) zurück.
    """
    try:
        konten = lade_konten_json()
        # Wir rufen einfach für jedes Objekt die neue to_dict() Methode auf
        return [k.to_dict() for k in konten]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden: {str(e)}")

@app.post("/transaktion/einzahlen/{name}", response_model=TransaktionErgebnis, tags=["2. Transaktionen"])
def einzahlen_api(
    name: str, 
    betrag: float = Query(description="Betrag, der eingezahlt werden soll")
):
    """
    **Einzahlung vornehmen**  
    - Prüft die Existenz des Kontos.
    - Aktualisiert den Kontostand unter Nutzung der Klassen-Logik.
    - Speichert die Änderungen dauerhaft in der JSON-Datenbank.
    """
    try:
        # 1. Daten laden
        konten = lade_konten_json()

        # 2. Konto suchen (DIESE Zeile wirft den ValueError, wenn nichts gefunden wird)
        k = finde_konto(konten, name)

        # 3. Logik ausführen
        nachricht = k.einzahlen(betrag)
        
        # 4. Speichern
        speichere_konten_json(konten)
        
        return {
            "nachricht": nachricht, 
            "inhaber": k.inhaber,
            "neuer_stand": k.kontostand
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")
        
    except Exception as e:
        # Nur echte Systemfehler landen hier (z.B. Festplatte voll beim Speichern)
        raise HTTPException(status_code=500, detail=f"❌ Systemfehler: {str(e)}")

@app.post("/transaktion/abheben/{name}", response_model=TransaktionErgebnis, tags=["2. Transaktionen"])
def abheben_api(
    name: str, 
    betrag: float = Query(description="Betrag, der abgehoben werden soll")
):
    """
    **Geld abheben**  
    Nutzt die Dispo-Logik des Girokontos oder die Sperre des Sparkontos.
    """
    try:
        konten = lade_konten_json()
        k = finde_konto(konten, name)
        # Hier greift eine Logik aus girokonto.py / sparkonto.py
        nachricht = k.abheben(betrag) 
        speichere_konten_json(konten)
        
        return {
            "nachricht": nachricht,
            "inhaber": k.inhaber,
            "neuer_stand": k.kontostand
        }
    except ValueError as e:
        # Hier fangen wir z.B. "Dispo überschritten" ab
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="❌ Interner Serverfehler")

@app.post("/konten/erstellen", tags=["3. Verwaltung"])
def konto_erstellen(daten: KontoErstellenSchema):
    """
    **Neues Konto erstellen**  
    Erzeugt ein neues Giro- oder Sparkonto-Objekt und speichert es in der Datenbank.
    """
    try:
        konten = lade_konten_json()
        typ = daten.typ.lower().strip()
        
        # Validierung und Erstellung (wie im interaktiven Menü)
        if typ == "giro":
            neues_k = Girokonto(daten.name, daten.start_saldo, daten.extra)
        elif typ == "spar":
            neues_k = Sparkonto(daten.name, daten.start_saldo, daten.extra)
        else:
            raise ValueError("⚠️ Ungültiger Kontotyp! Erlaubt sind 'giro' oder 'spar'.")
        
        konten.append(neues_k)
        speichere_konten_json(konten)
        
        return {"status": "✅ Erfolg", "details": f"Konto für {daten.name} ({typ}) erstellt."}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Systemfehler: {str(e)}")



@app.post("/zinsen/gutschreiben/{name}", tags=["4. Zinsen"])
def zinsen_gutschreiben(name: str):
    """
    **Zinsen fest verbuchen**  
    Berechnet die Zinsen für ein Sparkonto und aktualisiert den Kontostand dauerhaft.
    """
    try:
        konten = lade_konten_json()
        k = finde_konto(konten, name)
        
        # Wir prüfen, ob das Objekt die Methode 'zinsen_berechnen' besitzt
        if not hasattr(k, 'zinsen_berechnen'):
            raise ValueError(f"⚠️ Konto '{name}' ist kein Sparkonto und erhält keine Zinsen.")
            
        nachricht = k.zinsen_berechnen()
        speichere_konten_json(konten)
        
        return {"status": "✅ Erfolg", "details": nachricht, "neuer_stand": k.kontostand}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")



@app.post("/zinsen/simulieren/{name}", tags=["4. Zinsen"])
def zinsen_simulieren(name: str, sonderzins: float = Query(..., gt=0)):
    """
    **Sonderzins-Simulation**  
    Berechnet temporär Zinsen mit einem abweichenden Zinssatz (keine dauerhafte Änderung).
    """
    try:
        konten = lade_konten_json()
        k = finde_konto(konten, name)
        
        if not hasattr(k, 'zinsen_berechnen_mit'):
            raise ValueError(f"⚠️ Simulation für '{name}' nicht verfügbar (kein Sparkonto).")
            
        ergebnis = k.zinsen_berechnen_mit(sonderzins)
        return {"status": "✅ Simulation", "ergebnis": ergebnis}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")

