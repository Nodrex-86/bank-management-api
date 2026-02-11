# 🏦 Bank-Management API
A modular Python-based banking system featuring Object-Oriented Programming (OOP), automated testing, and interactive Menu

## 🌟 Current Features
- **OOP Core:** Robust class hierarchy for account management.
- **Account Types:** Specialized logic for Savings and Current accounts.
- **Validation:** Strict data handling using Python decorators.
- **Persistence:** Automated data handling using **JSON** for reliable storage between sessions.


## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Run the Application
Interactive CLI :

**Interactive Menu (CLI):**
```bash
python main.py
```

### 🌐 REST API (FastAPI)
The system offers a complete REST interface that maps all the functions of the CLI menu.

**Server starten:**
```bash
uvicorn api:app --reload
```
---

## 🧪 Testing
The project follows a modular structure where business logic and test suites are strictly separated. 

**Run the automated test suite from the root directory:**
```bash
python -m unittest discover -s tests
```

## 📚 Documentation
Technical documentation is auto-generated from docstrings using **pdoc**.

**To generate documentation for a specific file:**
```bash
pdoc ./[filename].py -o ./dokumentation
```
**To generate the latest documentation (Windows):**
Simply run the provided batch script:

**generate_docs.bat**

The output will be generated in the ./dokumentation folder.

---

## 📂 Project Structure

```text
Bank-Management-API/
├── tests/              # Automated Test Suites
│   ├── __init__.py
│   ├── test_banken.py
│   └── test_konto.py
├── main.py             # Logic controller
├── konto.py            # Base class with core validation logic
├── girokonto.py        # Specialized account type (Inheritance)
├── sparkonto.py        # Specialized account type (Inheritance)
└── konten.json         # JSON-based data storage (Persistence)
```


---
*Developed as a showcase for Python Backend Development, OOP