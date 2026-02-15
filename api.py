from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os
from pathlib import Path
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from json_storage import JSONStorage
from main import initialisiere_standard_konten, filtere_konten
from sparkonto import Sparkonto
from girokonto import Girokonto


# Globaler Storage-Provider (später einfach durch SQLiteStorage ersetzbar)
storage = JSONStorage("konten.json")

def stelle_datenbank_sicher():
    """Prüft, ob Daten vorhanden sind, sonst Initialisierung."""

    try:
        if not storage.laden():
            print("☁️ Initialisiere Standard-Datenbank...")
            standard = initialisiere_standard_konten()
            storage.speichern(standard)
    except Exception as e:
        print(f"Fehler be DB-Initialisierung: {e}")

stelle_datenbank_sicher()

app = FastAPI(
    title="🏦 Nodrex Bank-Management API",
    description="REST-Schnittstelle mit austauschbarem Storage-System (Repository Pattern), basierend auf OOP-Prinzipien",
    docs_url=None, # Wir deaktivieren die Standard-Doku kurz, um sie mit Icon zu laden
    version="1.3.0"
)

# --- SCHEMATA ---
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

# --- ENDPUNKTE ---

from fastapi.responses import HTMLResponse

@app.get("/", tags=["Allgemein"], response_class=HTMLResponse)
def home():
    """
    **Willkommens-Endpunkt**  
    Landing-Page mit Firmenlogo und Link zur Dokumentation.
    """
    return """
    <!DOCTYPE html>
    <html lang="de">
        <head>
            <meta charset="UTF-8">
            <title>Nodrex Bank API</title>
            <link rel="icon" href="/favicon.ico" type="image/x-icon">
            <style>
                body { 
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                    text-align: center; 
                    padding-top: 80px; 
                    background-color: #0f111a; /* Sehr dunkles Blau-Schwarz */
                    color: #e0e0e0;
                    margin: 0;
                }
                .container { 
                    background: #1c1f2b; /* Dunkles Anthrazit-Blau */
                    padding: 50px; 
                    border-radius: 20px; 
                    display: inline-block; 
                    box-shadow: 0 15px 35px rgba(0,0,0,0.5); 
                    max-width: 550px;
                    border-top: 4px solid #d32f2f; /* Roter Akzent-Balken oben */
                }
                .logo { 
                    max-width: 180px; 
                    height: auto; 
                    margin-bottom: 30px; 
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    filter: drop-shadow(0 0 10px rgba(255,255,255,0.1)); /* Hebt Silber leicht hervor */
                }
                h1 { color: #ffffff; margin-bottom: 15px; font-weight: 300; letter-spacing: 1px; }
                p { color: #b0b3b8; font-size: 1.1em; line-height: 1.6; }
                .btn { 
                    display: inline-block;
                    margin-top: 30px;
                    padding: 14px 28px;
                    background: #d32f2f; /* Dein Rot-Ton */
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
                }
                .btn:hover { 
                    background: #b71c1c; 
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(211, 47, 47, 0.4);
                }
                strong { color: #28a745; }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="/static/nr_logo.webp" alt="Nodrex Logo" class="logo">
                <h1>Nodrex Bank-Management API</h1>
                <p>Status: <span style="color: #28a745;">● Online</span></p>
                <p>Nutzen Sie die interaktive Dokumentation, um die Endpunkte zu testen:</p>
                <a href="/docs" class="btn">Zur Swagger Dokumentation</a>
            </div>
        </body>
    </html>
    """


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_favicon_url="/favicon.ico" # Hier verweisen wir auf deinen Endpunkt
    )

@app.get("/konten", tags=["1. Übersicht"])
def alle_konten():
    """
    **Alle Konten auflisten**  
    Gibt alle Konten dynamisch über den Storage-Provider zurück.
    """
    try:
        konten = storage.laden()
        return [k.to_dict() for k in konten] 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        konten = storage.laden()

        # 2. Konto suchen (DIESE Zeile wirft den ValueError, wenn nichts gefunden wird)
        k = storage.konto_holen(name)

        # 3. Logik ausführen
        nachricht = k.einzahlen(betrag)
        
        # 4. Speichern
        storage.speichern(konten)
        
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
        konten = storage.laden()
        k = storage.konto_holen(name)
        # Hier greift eine Logik aus girokonto.py / sparkonto.py
        nachricht = k.abheben(betrag) 
        storage.speichern(konten)
        
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
    

@app.get("/suche", tags=["3. Verwaltung"])
def api_suchen(name: str):
    """
    Sucht alle Konten, die den Suchbegriff im Namen enthalten.
    Gibt eine Liste der Treffer zurück.

    Args:
        name (str): Der Name des gesuchten Kontoinhabers.

    Returns:
        treffer: Gibt die Liste der Treffer zurück.
    """
    konten = storage.laden()
    treffer = filtere_konten(konten, name)
    if not treffer:
        return {"nachricht": "Keine Treffer", "ergebnisse": []}
    return treffer


@app.post("/konten/erstellen", tags=["3. Verwaltung"])
def konto_erstellen(daten: KontoErstellenSchema):
    """
    **Neues Konto erstellen**  
    Erzeugt ein neues Giro- oder Sparkonto-Objekt und speichert es in der Datenbank.
    """
    try:
        typ = daten.typ.lower().strip()
        
        # Validierung und Erstellung (wie im interaktiven Menü)
        if typ == "giro":
            neues_k = Girokonto(daten.name, daten.start_saldo, daten.extra)
        elif typ == "spar":
            neues_k = Sparkonto(daten.name, daten.start_saldo, daten.extra)
        else:
            raise ValueError("⚠️ Ungültiger Kontotyp! Erlaubt sind 'giro' oder 'spar'.")
        
        # Hier wird automatisch auf Duplikate geprüf
        storage.konto_hinzufuegen(neues_k)
        
        return {"status": "✅ Erfolg", "details": f"Konto für {daten.name} ({typ}) erstellt."}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")
    except Exception as e:
        print(f"DEBUG-ERROR: {type(e).__name__}: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"❌ Systemfehler: {str(e)}")


@app.post("/zinsen/gutschreiben/{name}", tags=["4. Zinsen"])
def zinsen_gutschreiben(name: str):
    """
    **Zinsen fest verbuchen**  
    Berechnet die Zinsen für ein Sparkonto und aktualisiert den Kontostand dauerhaft.
    """
    try:
        konten = storage.laden()
        k = storage.konto_holen(name)
        
        # Wir prüfen, ob das Objekt die Methode 'zinsen_berechnen' besitzt
        if not hasattr(k, 'zinsen_berechnen'):
            raise ValueError(f"⚠️ Konto '{name}' ist kein Sparkonto und erhält keine Zinsen.")
            
        nachricht = k.zinsen_berechnen()
        storage.speichern(konten)
        
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
        k = storage.konto_holen(name)
        
        if not hasattr(k, 'zinsen_berechnen_mit'):
            raise ValueError(f"⚠️ Simulation für '{name}' nicht verfügbar (kein Sparkonto).")
            
        ergebnis = k.zinsen_berechnen_mit(sonderzins)
        return {"status": "✅ Simulation", "ergebnis": ergebnis}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"⚠️ {str(e)}")
    
# --- STATISCHE DATEIEN & BROWSER-FIXES ---

@app.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
async def chrome_devtools_json():
    """Unterdrückt 404-Fehler durch Chrome DevTools Anfragen."""
    return Response(content="", media_type="application/json")

# Pfad zum Icon
BASE_DIR = Path(__file__).resolve().parent
FAVICON_PATH = BASE_DIR / "static" / "favicon.ico"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Liefert das Favicon aus oder sendet eine leere Antwort, um 404 zu vermeiden."""
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    return Response(content="", media_type="image/x-icon")

# Mounten für alle anderen statischen Dateien (z.B. Bilder für die Doku)
app.mount("/static", StaticFiles(directory="static"), name="static")
