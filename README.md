# 🏠 Baku Real Estate Price Estimator

An end-to-end machine learning project that predicts property prices in Baku, Azerbaijan. Built from scratch — from web scraping to a live deployed web app.

🔗 **[Live Demo](https://huggingface.co/spaces/Greenlight123/baku-property-estimator)**

---

## Overview

Property prices in Baku vary significantly based on location, size, floor, and condition. This project scrapes real listing data from [bina.az](https://bina.az), trains an XGBoost regression model, and serves predictions through an interactive Streamlit app with a clickable map.

---

## Results

| Metric | Value |
|--------|-------|
| R² Score | 0.80 |
| MAE | 41,150 AZN |
| MAPE | 14.18% |
| Training samples | 11,000+ |

---

## Data visualization

<img width="1915" height="950" alt="Image" src="https://github.com/user-attachments/assets/75afaf01-29d0-4bcf-9caa-6c03b13efaef" />

<img width="1917" height="947" alt="Image" src="https://github.com/user-attachments/assets/3bb0c058-d099-426d-99ca-e50d5eca51d1" />

---

## Features

- 🕷️ **Custom web scraper** — collects listings via GraphQL API with pagination
- 🗺️ **Interactive map** — users click to select property location
- 🚇 **Metro proximity** — automatically detects if property is within 1.5km of a metro station
- 🌐 **Live deployment** — hosted on Hugging Face Spaces

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Data collection | Python, Requests, BeautifulSoup, GraphQL |
| Data processing | Pandas, NumPy |
| Machine learning | XGBoost, Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Web app | Streamlit, Folium |
| Deployment | Hugging Face Spaces |

---

## Project Structure

```
── csv/
│   ├── data_with_address.csv
│   ├── final_data.csv
│   └── raw_data.csv
├── src/
│   ├── app.py                # Streamlit web application
│   ├── columns.pkl
│   └── REE_model.pkl         # Trained model weights
├── .env
├── .gitignore
├── getting_address.py        # For precise coordination, obtains address names via BeuatifulSoup
├── getting_coordinates.py    # Geocodes addresses via Nominatim
├── metro_proximity.py        # Calculates distance to metro
├── model.py                  # Trains and evaluates XGBoost model                 
├── README.md
├── requirements.txt
└── scraper.py                # Scrapes listings from bina.az
```

---

## How It Works

```
bina.az GraphQL API
        ↓
  Web Scraper (11k+ listings)
        ↓
  Data Cleaning & Feature Engineering
        ↓
  XGBoost Model Training
        ↓
  Streamlit App + Hugging Face Deployment
```

### Features used for prediction

| Feature | Description |
|---------|-------------|
| Area (m²) | Property size |
| Rooms | Number of rooms |
| Floor | Which floor (apartments only) |
| Total floors | Building height (apartments only) |
| Repaired | Whether property is renovated |
| Latitude & Longitude | Exact location from map click |
| Metro proximity | Within 1.5km of metro station |
| Location | District (one-hot encoded, 100+ districts) |

---

## Installation

```bash
git clone https://github.com/FuadGanbarli/baku-property-estimator.git
cd baku-property-estimator
pip install -r requirements.txt
```

### Run the app locally

```bash
python -m streamlit run app.py
```

### Scrape fresh data

```bash
python scraper.py
```

> ⚠️ You'll need a valid `_binaaz_session` cookie from bina.az to run the scraper.

---

## Model Development

The model went through several iterations:

| Version | R² | MAE | MAPE |
|---------|-----|-----|------|
| Baseline | 0.578 | 53,332 AZN | 18.79% |
| + Outlier removal | 0.729 | 43,999 AZN | 16.86% |
| + Log transformation | 0.828 | 41,386 AZN | 15.58% |
| + One-hot encoding | 0.862 | 35,373 AZN | 12.98% |
| Final | **0.797** | **41,150 AZN** | **14.18%** |

Key improvements:
- Log transforming the target variable (price) to handle skewed distribution
- One-hot encoding for location instead of label encoding
- Removing top/bottom 1% price outliers
- Separate models for apartments vs houses

---

## App Screenshot

> User selects location on map, fills in property details, and gets an instant price estimate in AZN.
<img width="1139" height="746" alt="Image" src="https://github.com/user-attachments/assets/77447f14-fac1-4072-bf21-1a152b94ef40" />
---

## Future Improvements

- [ ] Scrape more data (80k+ listings available)
- [ ] Fix coordinate accuracy with better geocoding
- [ ] Add price trend over time
- [ ] Add price per m² prediction
- [ ] Mobile-friendly UI

---

## License

MIT License — feel free to use, modify, and distribute.

---

## Author

Built by [FuadGanbarli](https://github.com/FuadGanbarli) as a portfolio project.
