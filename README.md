# 🏦 Bank-Management API
A modular Python-based banking system demonstrating Object-Oriented Programming (OOP) principles.

## 🌟 Current Features
- **OOP Core:** Robust class hierarchy for account management.
- **Account Types:** Specialized logic for Savings and Current accounts.
- **Validation:** Strict data handling using Python decorators.



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