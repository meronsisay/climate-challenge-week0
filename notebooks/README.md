# Climate Analysis Notebooks

## Overview
This directory contains exploratory data analysis (EDA) notebooks for five East African countries and a cross-country comparison analysis for COP32 climate vulnerability assessment.

## Data Source
- **Original data:** NASA POWER (Prediction Of Worldwide Energy Resources)
- **Variables:** Temperature (T2M, T2M_MAX, T2M_MIN), Precipitation (PRECTOTCORR), Humidity (RH2M), Wind Speed (WS2M, WS2M_MAX)
- **Time period:** 2015-2026
- **Countries:** Ethiopia, Kenya, Nigeria, Sudan, Tanzania

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
