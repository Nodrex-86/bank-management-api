import sqlite3
import random
from storage_interface import StorageInterface
from logger_config import logger
from sparkonto import Sparkonto
from girokonto import Girokonto


class SQLiteStorage(StorageInterface):
    def __init__(self, db_path="bank_data.db"):
        self.db_path = db_path
        self._initialisiere_tabelle()

    def _initialisiere_tabelle(self):
        """
        Erstellt die Tabelle, falls sie noch nicht existiert.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS konten (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        inhaber TEXT NOT NULL UNIQUE,
                        kontostand REAL NOT NULL,
                        typ TEXT NOT NULL,
                        extra_wert REAL
                    )
                """)
                conn.commit()
                logger.info("SQLite-Datenbank erfolgreich initialisiert.")
        except Exception as e:
            logger.error(f"Fehler bei der SQL-Initialisierung: {e}")

    def speichern(self, konten_liste):
        """
        Synchronisiert eine Liste von Konten mit der Datenbank.
        Nutzt 'INSERT OR REPLACE', um existierende Konten zu aktualisieren 
        und neue Konten hinzuzufügen (Upsert-Logik).

        Args:
            konten_liste (list): Liste der Girokonto- oder Sparkonto-Objekte.

        Raises:
            IOError: Wenn die Datei nicht geschrieben werden kann.
        """
        if not konten_liste:
            logger.info("SQLite: Keine Konten zum Speichern übergeben.")
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for konto in konten_liste:
                    # Bestimme den Extra-Wert (Dispo oder Zins)
                    extra = getattr(konto, 'dispo', getattr(konto, 'zins', 0))
                    
                    # 'INSERT OR REPLACE' nutzt den UNIQUE-Constraint auf 'inhaber'
                    cursor.execute("""
                        INSERT OR REPLACE INTO konten (inhaber, kontostand, typ, extra_wert)
                        VALUES (?, ?, ?, ?)
                    """, (konto.inhaber, konto.kontostand, type(konto).__name__, extra))
                
                conn.commit()
                logger.info(f"SQLite: Synchronisation von {len(konten_liste)} Konten abgeschlossen.")
        except Exception as e:
            logger.error(f"Fehler beim SQL-Synchronisieren: {e}")
            raise IOError(f"Datenbank-Synchronisation fehlgeschlagen: {e}")


    def laden(self) -> list:
        """
        Lädt alle Konten aus der SQLite-Datenbank und wandelt sie in Objekte um.
        """
        konten_liste = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row # Erlaubt Zugriff via Spaltennamen
                cursor = conn.cursor()
                cursor.execute("SELECT * from konten")
                zeilen = cursor.fetchall()

                for row in zeilen:
                    # Mapping: Datenbank-Spalten -> Python-Objekt-Attribute
                    if row["typ"] == "Girokonto":
                        k = Girokonto(row["inhaber"], row["kontostand"], row["extra_wert"])
                    else:
                        k = Sparkonto(row["inhaber"], row["kontostand"], row["extra_wert"])
                    konten_liste.append(k)

                logger.info(f"SQLite: {len(konten_liste)} Konten erfolgreich geladen.")
                return konten_liste
        except Exception as e:
            logger.error(f"Fehler beim Laden aus SQLite: {e}")
            return []
        
    def konto_holen(self, name):
        """
        Sucht ein Konto in der SQLite-Datenbank und gibt ein Objekt zurück.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.

        Raises:
            ValueError: Wenn Konto-Objekt ist None und kein Treffer erzielt wurde.

        Returns:
            object: Das gefundene Konto-Objekt.
        """
        try: 
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM konten WHERE LOWER(inhaber) = LOWER(?)", (name.strip().lower(),))
                row = cursor.fetchone()

                if row is None:
                    raise ValueError(f"Konto für '{name}' wurde nicht gefunden.")
                
                # Mapping SQL -> Objekt
                if row["typ"] == "Girokonto":
                    return Girokonto(row["inhaber"], row["kontostand"], row["extra_wert"])
                else:
                    return Sparkonto(row["inhaber"], row["kontostand"], row["extra_wert"])
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"SQLite Fehler beim Holen von {name}: {e}")
            raise RuntimeError("Interner Datenbankfehler.")
    
    def konto_hinzufuegen(self, konto):
        """
        Speichert ein neues Konto permanent in der Datenbank.

        Args:
            konto (object): Das Konto-Objekt (Giro- oder Sparkonto), das hinzugefügt werden soll.
        """
        # Wird bestehende Logik für die Vorschläge (UX) verwendet.
        if self.name_existiert(konto.inhaber):
            vorschlaege = self.generiere_vorschlaege(konto.inhaber)
            raise ValueError(f"Name existiert bereits. Vorschläge: {', '.join(vorschlaege)}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                extra = getattr(konto, 'dispo', getattr(konto, 'zins', 0))
                # WICHTIG: Das Tupel am Ende muss GENAU 4 Werte enthalten
                werte = (konto.inhaber, konto.kontostand, type(konto).__name__, extra)
                cursor.execute("""
                    INSERT INTO konten (inhaber, kontostand, typ, extra_wert)
                    VALUES (?, ?, ?, ?)
                """, werte)
                conn.commit()
                logger.info(f"SQLite: Konto für {konto.inhaber} erfolgreich angelegt.")
        except sqlite3.IntegrityError:
            # Falls der Name-Check oben (Race Condition) versagt, greift das UNIQUE-Constraint der DB
            logger.warning(f"SQL IntegrityError: Name {konto.inhaber} bereits vergeben.")
            raise ValueError(f"Datenbank-Fehler: Name '{konto.inhaber}' ist bereits vergeben.")
        except Exception as e:
            logger.error(f"Fehler beim SQL-Insert: {e}")
            raise RuntimeError("Konto konnte nicht gespeichert werden.")
        
    def name_existiert(self, name):
        """
        Performanter Check auf Datenbank-Ebene.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM konten WHERE LOWER(inhaber) = LOWER(?) LIMIT 1", (name.strip(),))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Fehler beim Namen-Check: {e}")
            return False
        
    def generiere_vorschlaege (self, name):
        """
        Erzeugt 3 Namensvorschläge mit Zufallszahlen, die in der SQL-DB noch nicht existieren.

        Args:
            name (str): Der Name des gesuchten Kontoinhabers.
        """
        vorschlaege = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                while len(vorschlaege) < 3:
                    nr = random.randint(10, 99)
                    neuer_name = f"{name}{nr}"

                    # Schneller Check in der Datenbank
                    cursor.execute("SELECT 1 FROM konten WHERE LOWER(inhaber) = LOWER(?) LIMIT 1", (neuer_name,))
                    if cursor.fetchone() is None:
                        if neuer_name not in vorschlaege:
                            vorschlaege.append(neuer_name)
                return vorschlaege
        except Exception as e:
            logger.error(f"Fehler dei der Generierung vovn VOrschlägen (SQL): {e}")
            return [f"{name}11", f"{name}22", f"{name}33"] # Fallback

    def update_kontostand(self, konto):
        """
        Aktualisiert nur den Kontostand eines existierenden Kontos in der Datenbank.

        Args:
            konto (object): Das Konto-Objekt (Giro- oder Sparkonto) die upgedated werden soll.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE konten
                    SET kontostand = ?
                    WHERE LOWER(inhaber) = LOWER(?)
                """, (konto.kontostand, konto.inhaber))
                conn.commit()
                logger.info(f"SQLite Update: Kontostand für {konto.inhaber} aktualisiert.")
        except Exception as e:
            logger.error(f"Fehler beim SQL-Update für {konto.inhaber}: {e}")