# Climate Change Analysis: East Africa (2015–2026)

## Project Overview
This repository analyzes climate trends, seasonal variations, and extreme weather patterns across East Africa using NASA POWER meteorological data (2015-2026). The project covers temperature, precipitation, humidity, and wind speed to inform climate vulnerability assessment and adaptation strategies.

**Countries analyzed:** Ethiopia, Kenya, Nigeria, Sudan, Tanzania

---

## Key Findings

### Temperature Rankings
| Rank | Country | Mean Temp | Std Dev |
|------|---------|-----------|---------|
| 1 | Sudan | 28.76°C | 4.68 |
| 2 | Tanzania | 26.80°C | 1.33 |
| 3 | Nigeria | 26.66°C | 1.12 |
| 4 | Kenya | 20.43°C | 1.44 |
| 5 | Ethiopia | 16.07°C | 1.90 |

### Precipitation Rankings
| Rank | Country | Mean (mm/day) | Std Dev |
|------|---------|---------------|---------|
| 1 | Nigeria | 4.21 | 7.27 |
| 2 | Tanzania | 3.74 | 8.00 |
| 3 | Ethiopia | 3.63 | 6.29 |
| 4 | Kenya | 1.47 | 3.18 |
| 5 | Sudan | 0.64 | 3.06 |

### Vulnerability Ranking (1 = Most Vulnerable)
| Rank | Country | Heat Risk | Drought Risk |
|------|---------|-----------|--------------|
| 1 | Sudan | Extreme | Extreme |
| 2 | Nigeria | None | High |
| 3 | Tanzania | None | High |
| 4 | Kenya | None | Low |
| 5 | Ethiopia | None | Low |

### Statistical Validation
- **ANOVA Test:** F = 18,938.75, p < 0.001
- **Conclusion:** Significant temperature differences exist across all countries

---

## Repository Structure

## **Repository Structure**
climate-challenge-week0/
├── .github/workflows/ # CI/CD configuration
├── data/ # Raw and cleaned CSV files (git-ignored)
├── notebooks/ # Jupyter notebooks for EDA and comparison
├── scripts/ # Utility scripts
├── tests/ # Unit tests
├── .gitignore
├── requirements.txt
└── README.md

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

## Notebooks

### Individual Country EDA
- `ethiopia_eda.ipynb`
- `kenya_eda.ipynb`
- `nigeria_eda.ipynb`
- `sudan_eda.ipynb`
- `tanzania_eda.ipynb`

**Each notebook performs:**
- Data loading and date parsing
- Missing value handling (-999 → NaN)
- Outlier detection (Z-score method)
- Time series analysis
- Correlation analysis
- Distribution analysis
- Export cleaned data

### Cross-Country Comparison
- `compare_countries.ipynb`

**Includes:**
- Temperature trend comparison
- Precipitation variability analysis
- Extreme event frequency (heat days, dry spells)
- Statistical testing (ANOVA)
- Vulnerability ranking
- Policy recommendations

---

## Data Processing

### Source
- **Dataset:** NASA POWER (Prediction Of Worldwide Energy Resources)
- **Variables:** T2M, T2M_MAX, T2M_MIN, PRECTOTCORR, RH2M, WS2M, WS2M_MAX
- **Time period:** 2015-2026
- **Missing value sentinel:** -999

### Cleaning Steps
- Converted YEAR + DOY to datetime
- Replaced -999 with NaN
- Removed duplicate rows
- Applied Z-score outlier detection (|Z| > 3)
- Forward-filled missing weather variables

---

## CI/CD Pipeline

GitHub Actions runs on every push to `main`:
- Sets up Python 3.10
- Installs dependencies from `requirements.txt`
- Verifies Python version

**Status:** ✅ Passing

---

## Dependencies
- numpy==2.1.3
- pandas==2.2.3
- matplotlib==3.10.0
- seaborn==0.13.2
- scipy==1.15.2
- jupyter==1.1.1
- ipykernel==6.29.5


---

## COP32 Recommendations

1. **Sudan** requires urgent heat action plan (28.8°C mean, extreme heat days)
2. **Tanzania** needs flood early warning systems (most variable precipitation, σ=8.0)
3. **Ethiopia's highlands** serve as climate refuge (16.1°C mean, stable rains)
4. **Sudan** should receive priority climate finance (compound heat-drought crisis)

---

## Author

Meron Sisay

---

## Acknowledgments

- NASA POWER for meteorological data
- COP32 preparation team