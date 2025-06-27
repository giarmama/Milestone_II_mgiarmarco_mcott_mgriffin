# Predicting the Impact of Air Quality on Public Transportation Usage

**Team 9 – SIADS 693: Milestone II**  

## Project Overview

This project investigates the relationship between air quality and public transportation ridership in two U.S. cities: Chicago and New York. Using historical weather, air quality, and transit data from 2023–2024, we aim to evaluate the extent to which environmental factors can explain or predict daily ridership patterns.

Our methodology combines:
- **Feature engineering** of lagged, binned, and calendar-aware variables
- **Unsupervised learning** via DBSCAN and Agglomerative Clustering
- **Supervised learning** using Lasso Regression, Random Forest, and XGBoost

## Required Libraries

Install the following Python packages:

pip install pandas numpy scikit-learn xgboost shap matplotlib seaborn requests_cache geopy openmeteo-requests

##  Data Sources

- **Air Quality & Weather:**  
  [Open-Meteo Historical Forecast API](https://historical-forecast-api.open-meteo.com)  
  [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com)

- **Public Transportation:**  
  [Chicago CTA Ridership](https://data.cityofchicago.org)  
  [NYC MTA Ridership](https://data.ny.gov)

## 👥 Team Members
- **Mark Griffin** – 
  - Data Acquisition (Public Transportation)
  - Unsupervised Learning (DBSCAN, Agglomerative Clustering)
  - Supervised Learning (Lasso)
- **Matt Cott** 
  - Supervised Learning (XGBoost)
  - SHAP
  - Failure analysis  
  - Feature Ablation
- **Michael Giarmarco** 
  - Data Acquisition (Air Quality, Weather)
  - Feature Engineering (Truncated SVD, lag and holiday features)
  - Unsupervised Learning (Principal Component Analysis)
  - Supervised Learning (Random Forest)
  
