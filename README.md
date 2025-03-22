# 🚖 Uber Trip Analysis Report

This project performs an simple and in-depth analysis of Uber trip data exported from my personal account. It summarizes trip durations, locations, and patterns over time while visualizing geographic clusters of pickups and drop-offs using interactive maps.

---

## 🔍 Project Overview

- **Data Source:** `trips_data-0.csv` exported from Uber's data portal
- **Tooling:** Python, Pandas, Matplotlib, Seaborn, scikit-learn (KMeans), Folium
- **Code:** The full analysis and logic is implemented in [`uber_analysis.py`](uber_analysis.py)
- **Goal:** Extract trends from trip data and visualize the most common locations and behaviors over time

---

## 🧠 Methodology

### 🧼 1. Data Cleaning
- Removed trips with statuses: `rider_canceled`, `driver_canceled`, or `unfulfilled`
- Replaced missing addresses with latitude/longitude fallback values
- Converted timestamps to datetime objects for easier manipulation
- Calculated `trip_duration` in minutes from start and end times

---

### 🗺️ 2. Location Analysis
- Identified **most common pickup and drop-off addresses**
- Cleaned ZIP code suffixes (e.g., `-1234`) for better grouping
- Calculated frequency of trips by:
  - **Hour of the day**
  - **Day of the week**

---

### 📊 3. Visualizations
All graphs are saved in the `MyGraphs` folder:
- Distribution of trip durations
- Trips per hour of the day
- Trips per day of the week
- Elbow plots to determine optimal `k` for clustering locations

---

### 📍 4. Geographic Clustering (KMeans)
- Applied **KMeans clustering** to both pickup and drop-off GPS coordinates
- Used the **elbow method** to determine `k = 4` as the optimal cluster count
- Created two interactive Folium maps:

---

## 🌐 Interactive Maps

- **[Clustered Uber Map](https://paulgarces.github.io/MyUberData/uber_clusters_map.html)**  
  Shows pickup/drop-off location clusters using KMeans

- **[My Uber Trip Map](https://paulgarces.github.io/MyUberData/myubermap.html)**  
  Displays all individual trips with start/end markers, timestamps, and route lines

---

## 📁 File Structure

| File/Folder           | Purpose                                     |
|------------------------|---------------------------------------------|
| `trips_data-0.csv`     | Raw Uber trip data                         |
| `uber_analysis.py`     | Full code for data cleaning, analysis, mapping |
| `README.md`            | This report (auto-generated)               |
| `MyGraphs`            | Contains saved graphs                      |

---

## 📊 General Trip Summary

- **Total Trips:** 161  
- **Average Trip Duration:** 13.94 minutes  
- **Longest Trip:** 85.95 minutes, covering **54.21 miles**  
  - **Pickup:** Calle de Agustín de Foxá 31, 28036 Madrid, ES  
  - **Drop-off:** C. Marqués del Arco, 1, 40001 Segovia, Spain  

- **Shortest Trip:** 1.35 minutes, covering **0.28 miles**  
  - **Pickup:** 1130 SE Everett Mall Way Ste A, Everett, WA 98208, US  
  - **Drop-off:** 1405 SE Everett Mall Way, Everett, WA 98208, US  

- **First Recorded Trip:** 2021-06-25 21:18:17  
- **Most Recent Trip:** 2025-02-05 09:35:13

---

## 🗺️ Most Common Locations

### Most Frequent Pickup Locations:
- 1029 NE 62nd St, Seattle, WA 98115, US (24 times)  
- 1500 Broadway, Seattle, WA 98122, US (4 times)  
- Grant Ln, Seattle, WA 98195, US (2 times)  
- Clark Rd, Seattle, WA 98195, US (2 times)  
- All Terminals (2 times)

### Most Frequent Dropoff Locations:
- 1029 NE 62nd St, Seattle, WA 98115, US (77 times)  
- 4245 Roosevelt Way NE 2nd floor w220, Seattle, WA 98105, USA (8 times)  
- 4000 15th Ave NE, Seattle, WA 98195, US (7 times)  
- Main Terminal, Seattle-Tacoma International Airport (SEA), Seattle, WA (6 times)  
- Central Terminal, Seattle-Tacoma International Airport (SEA), Seattle (5 times)

---

## 🕒 Uber Trips by Hour

- **Peak Hour:** 8:00 AM (23 trips)  
- **Least Busy Hour:** 11:00 AM (2 trips)

---

## 📅 Uber Trips by Day of the Week

- **Busiest Day:** Sunday (35 trips)  
- **Least Busy Day:** Tuesday (10 trips)

**Trips per day:**
- Sunday (35)
- Saturday (29)
- Wednesday (27)
- Friday (24)
- Thursday (23)
- Monday (13)
- Tuesday (10)

---