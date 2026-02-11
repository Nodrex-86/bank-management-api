# 🏦 Bank-Management API ![Python CI](https://github.com/Nodrex-86/bank-management-api/actions/workflows/python-app.yml/badge.svg)

A modular Python-based banking system featuring Object-Oriented Programming (OOP), automated testing, and a modern REST API interface.

## 🌐 Live Demo & Cloud Infrastructure
The application is containerized and automatically deployed to the cloud using a custom CI/CD pipeline.

- **Live API Documentation:** 👉 [Interactive Swagger UI (Azure)](https://nodrex-management-api-ddhqgfgtg6b4c7hm.westeurope-01.azurewebsites.net/docs)
- **Deployment Status:** [![Build and Deploy FastAPI to Azure](https://github.com/Nodrex-86/bank-management-api/actions/workflows/main.yml/badge.svg)](https://github.com/Nodrex-86/bank-management-api/actions/workflows/main.yml)

### 🛠️ Tech Stack (Cloud)
- **Cloud Provider:** Microsoft Azure (App Services)
- **Container Registry:** GitHub Container Registry (GHCR)
- **CI/CD Pipeline:** GitHub Actions (Automated Docker Build & Push)
- **Security:** Azure Service Principals (RBAC)

## 🌟 Key Features
- **OOP Core:** Robust class hierarchy (Inheritance) with strict data validation using Python Decorators (@property/@setter).
- **REST API:** Modern web interface built with **FastAPI** and asynchronous support.
- **Persistence:** Automated data handling using **JSON** for reliable storage.
- **Quality Assurance:** Full test coverage with automated **Unit-Tests**.
- **Documentation:** Auto-generated technical documentation via **pdoc**.
- **Cloud Ready:** Includes **Docker** configuration for seamless deployment (e.g., Azure).

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can choose between the Interactive CLI or the Web API:

**Interactive Menu (CLI):**
```bash
python main.py
```

**REST API (FastAPI):**
```bash
uvicorn api:app --reload
```
Once started, access the **Interactive API Documentation (Swagger)** at:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing
The project follows a modular structure where business logic and test suites are strictly separated. Automated tests ensure the reliability of both account logic and API endpoints.

**Prerequisites:**
- **API testing requires** `httpx` (included in `requirements.txt`).
- **Note:** The database (`konten.json`) is automatically initialized with default data if it is missing during the test run.
### Run all tests (Logic & API) from the root directory:
```bash
python -m unittest discover -s tests
```

---

## 🐳 Docker Deployment
Build and run the containerized application locally:
```bash
docker build -t bank-api .
docker run -p 8000:8000 bank-api
```

## 📚 Documentation
Technical documentation is auto-generated from docstrings using **pdoc**.

**To generate documentation for a specific file:**
```bash
pdoc ./[filename].py -o ./dokumentation
```
**To generate the latest documentation (Windows):**
Simply run the provided batch script:
```bash
generate_docs.bat
```
The output will be generated in the ./dokumentation folder.

---

## 📂 Project Structure

```text
Bank-Management-API/
├── .github/workflows/  # CI/CD Pipeline Definitions
    ├── main.yml
├── tests/              # Automated Test Suites
│   ├── __init__.py
│   ├── test_banken.py
│   └── test_konto.py
├── api.py              # FastAPI implementation & REST Endpoints
├── main.py             # Logic controller & Interactive CLI
├── konto.py            # Base class with core validation logic
├── girokonto.py        # Specialized account type (Inheritance)
├── sparkonto.py        # Specialized account type (Inheritance)
├── requirements.txt    # Project dependencies
├── Dockerfile          # Containerization for Cloud/DevOps
└── konten.json         # JSON-based data storage (Persistence)
```


---
*Developed as a showcase for Python Backend Development, OOP
