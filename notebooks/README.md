# Analysis Notebooks

This directory contains the core exploratory data analysis (EDA) and statistical modeling for the East Africa climate study. The notebooks transform raw NASA POWER meteorological data into actionable climate insights.

## **Notebooks Overview**

### **1. ethiopia_eda.ipynb**
This notebook provides a comprehensive assessment of the Ethiopian Highlands' climate profile from 2015 to 2026.

* **Data Scope:** 4,108 daily observations of temperature, precipitation, humidity, and wind speed.
* **Key Methodologies:**
    * **Outlier Management:** Statistical identification using Z-scores ($|Z| > 3$) and IQR, with a focus on retaining climate signals (extreme weather events).
    * **Trend Analysis:** Linear regression modeling to determine the regional warming rate.
    * **Seasonality Profiling:** Visualization of bimodal rainfall regimes (*Kiremt* and *Bega*) using line charts and monthly boxplots.
    * **Correlation Studies:** Analysis of the feedback loops between thermal intensity and atmospheric moisture.
* **Primary Findings:**
    * **Warming Rate:** Identified a sustained warming trend of **0.0160°C per year**.
    * **Thermal Correlation:** A strong negative correlation (**-0.79**) between Maximum Temperature ($T2M\_MAX$) and Relative Humidity ($RH2M$), indicating significant evapotranspiration stress during peak heat months.

## **Usage Instructions**

### **Dependencies**
These notebooks require the following Python stack:
* `pandas` & `numpy` (Data Processing)
* `matplotlib` & `seaborn` (Visualization)
* `scipy.stats` (Statistical Modeling)

### **Execution**
To run the notebooks locally:
1.  Ensure your virtual environment is active.
2.  Launch the Jupyter interface:
    ```bash
    jupyter notebook
    ```
3.  Open `ethiopia_eda.ipynb` to view the finalized Task 2 analysis.

---

## **Data Integrity Note**
All analysis within these notebooks is performed on validated datasets. Outliers have been cross-referenced against geographic physical bounds to ensure that extreme meteorological events are accurately represented without being skewed by potential sensor malfunctions.