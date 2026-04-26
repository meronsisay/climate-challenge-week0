# Climate Change Analysis: East Africa (2015–2026)

## **Project Overview**
This repository is dedicated to identifying and quantifying climate trends, seasonal variations, and extreme weather patterns across East Africa. Using the **NASA POWER** meteorological dataset, the project applies statistical profiling and exploratory data analysis (EDA) to inform agricultural resilience and urban adaptation strategies.

The analysis covers key climate variables including temperature (T2M), precipitation (PRECTOTCORR), humidity (RH2M), and wind speed (WS2M) from 2015 through early 2026.

---

## **Repository Structure**
* **.github/**: CI/CD configurations and GitHub Actions.
* **notebooks/**: Comprehensive Jupyter notebooks for regional analysis and visualization.
* **scripts/**: Python utility scripts for data acquisition and preprocessing.
* **tests/**: Unit tests ensuring data integrity and function reliability.
* **requirements.txt**: Project dependencies and library versions.

---

## **Environment Setup**

### **Prerequisites**
* Python 3.10+
* Git

1. **Clone the repository:**
   ```bash
   git clone https://github.com/meronsisay/climate-challenge-week0.git
   cd climate-challenge-week0
2. Create venv: `python -m venv venv`
3. Activate venv:
   - Windows (Git Bash): `source venv/Scripts/activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`