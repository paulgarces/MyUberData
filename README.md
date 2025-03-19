# 🚖 Uber Trip Analysis Report

## 📝 About This Repository

This repository contains an analysis of my Uber trips using Python.  

- **Main Python Script:** All code and logic for processing, analyzing, and visualizing the data is located in **`uber_analysis.py`**.
- **HTML Files:** The `.html` files are **dynamically generated map visualizations**. They are **not part of the core analysis** but serve as interactive outputs for geospatial insights.

## 📊 General Trip Summary

- **Total Trips:** 161
- **Average Trip Duration:** 13.94 minutes
- **Longest Trip:** 85.95 minutes, covering **54.21 miles**
  - **Pickup:** Calle de Agustín de Foxá 31, 28036 Madrid, ES
  - **Drop-off:** C. Marqués del Arco, 1, 40001 Segovia, Spain
- **Shortest Trip:** 1.35 minutes, covering **0.28 miles**
  - **Pickup:** 1130 SE Everett Mall Way Ste A, Everett, WA 98208, US
  - **Drop-off:** 1405 SE Everett Mall Way, Everett, WA 98208, US
- **First Recorded Trip (by Year):** 2021-06-25 21:18:17+00:00
- **Most Recent Trip (by Year):** 2025-02-05 09:35:13+00:00

## 🗺️ Most Common Locations

- **Most common pickup locations:**
  - 1029 NE 62nd St, Seattle, WA 98115, US (24 times)
  - 1500 Broadway, Seattle, WA 98122, US (4 times)
  - Grant Ln, Seattle, WA 98195, US (2 times)
  - Clark Rd, Seattle, WA 98195, US (2 times)
  - All Terminals (2 times)

- **Most common dropoff locations:**
  - 1029 NE 62nd St, Seattle, WA 98115, US (77 times)
  - 4245 Roosevelt Way NE 2nd floor w220, Seattle, WA 98105, USA (8 times)
  - 4000 15th Ave NE, Seattle, WA 98195, US (7 times)
  - Main Terminal, Seattle-Tacoma International Airport (SEA), Seattle, WA (6 times)
  - Central Terminal, Seattle-Tacoma International Airport (SEA), Seattle (5 times)
## 🕒 Uber Trips by Hour

- **Peak Hour:** 8:00 AM (23 trips)
- **Least Busy Hour:** 11:00 AM (2 trips)

## 📅 Uber Trips by Day of the Week

- **Busiest Day:** Sunday (35 trips)
- **Least Busy Day:** Tuesday (10 trips)

- **Trips per day:**
  - Sunday (35 trips)
  - Saturday (29 trips)
  - Wednesday (27 trips)
  - Friday (24 trips)
  - Thursday (23 trips)
  - Monday (13 trips)
  - Tuesday (10 trips)

## 🌍 Clustered Uber Map

- Using the **elbow method**, I determined that the optimal number of clusters for pickup and drop-off locations is **4**.

🔗 [Click here to view the Clustered Uber Map](https://paulgarces.github.io/MyUberData/uber_clusters_map.html)

## 🗺️ Interactive Uber Map

🔗 [Click here to view my Uber trip map](https://paulgarces.github.io/MyUberData/myubermap.html)

