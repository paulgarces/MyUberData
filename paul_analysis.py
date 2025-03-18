import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import folium
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from folium.plugins import MarkerCluster
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import os
import sys

pd.set_option('display.max_columns', None)

uber_data = pd.read_csv("/Users/paulgarces/Desktop/uber_data/Rider/trips_data-0.csv")

repo_path = os.path.expanduser("~/Desktop/MyUberData")
graphs_path = os.path.join(repo_path, "MyGraphs")
report_path = os.path.join(repo_path, "My Uber Trip Analysis.md")

os.makedirs(graphs_path, exist_ok=True)

sys.stdout = open(report_path, "w")

uber_data.dropna(inplace=True)
uber_data['trip_start_time'] = pd.to_datetime(uber_data['begin_trip_time'])
uber_data['trip_end_time'] = pd.to_datetime(uber_data['dropoff_time'])
uber_data['request_time'] = pd.to_datetime(uber_data['request_time'])

uber_data['hour'] = uber_data['trip_start_time'].dt.hour
uber_data['day_of_week'] = uber_data['trip_start_time'].dt.day_name()
uber_data['month'] = uber_data['trip_start_time'].dt.month_name()
uber_data['trip_duration'] = (uber_data['trip_end_time'] - uber_data['trip_start_time']).dt.total_seconds() / 60

print("# 🚖 Uber Trip Analysis Report\n")

print("## 📊 General Trip Summary\n")
print(f"- **Total Trips:** {len(uber_data)}")
print(f"- **Average Trip Duration:** {uber_data['trip_duration'].mean():.2f} minutes")
print(f"- **Longest Trip:** {uber_data['trip_duration'].max():.2f} minutes")
print(f"- **Shortest Trip:** {uber_data['trip_duration'].min():.2f} minutes")
print(f"- **Earliest Trip:** {uber_data['trip_start_time'].min()}")
print(f"- **Latest Trip:** {uber_data['trip_end_time'].max()}\n")

most_common_pickup = uber_data['begintrip_address'].mode()[0]
most_common_dropoff = uber_data['dropoff_address'].mode()[0]

print("## 🗺️ Most Common Locations\n")
print(f"- **Most common pickup location:** {most_common_pickup}")
print(f"- **Most common dropoff location:** {most_common_dropoff}\n")

peak_hour = uber_data['hour'].mode()[0]
low_hour = uber_data['hour'].value_counts().idxmin()

print("## 🕒 Uber Trips by Hour\n")
print(f"- **Peak Hour:** {peak_hour}:00")
print(f"- **Least Busy Hour:** {low_hour}:00\n")

busiest_day = uber_data['day_of_week'].value_counts().idxmax()
least_busy_day = uber_data['day_of_week'].value_counts().idxmin()

print("## 📅 Uber Trips by Day of the Week\n")
print(f"- **Busiest Day:** {busiest_day}")
print(f"- **Least Busy Day:** {least_busy_day}\n")

plt.figure(figsize=(8,5))
sns.histplot(uber_data['trip_duration'], bins=30)
plt.xlabel("Trip Duration (minutes)")
plt.ylabel("Number of Trips")
plt.title("Distribution of Uber Trip Durations")
plt.savefig(os.path.join(graphs_path, "trip_duration_distribution.png"))
plt.close()

plt.figure(figsize=(10,5))
sns.countplot(x='hour', data=uber_data)
plt.title("Uber Trips by Hour of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Trips")
plt.savefig(os.path.join(graphs_path, "trips_by_hour.png"))
plt.close()

plt.figure(figsize=(10,5))
sns.countplot(x='day_of_week', data=uber_data, 
              order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title("Uber Trips by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Trips")
plt.savefig(os.path.join(graphs_path, "trips_by_day.png"))
plt.close()

pickup_coords = uber_data[['begintrip_lat', 'begintrip_lng']]
dropoff_coords = uber_data[['dropoff_lat', 'dropoff_lng']]

k_values = range(1, 11)

wcss_pickup = []
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pickup_coords)
    wcss_pickup.append(kmeans.inertia_)

wcss_dropoff = []
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(dropoff_coords)
    wcss_dropoff.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(k_values, wcss_pickup, marker='o', linestyle='-')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
plt.title("Elbow Method for Pickup Locations")
plt.grid()
plt.savefig("pickup_elbow_method.png")
# plt.show()

plt.figure(figsize=(8, 5))
plt.plot(k_values, wcss_dropoff, marker='o', linestyle='-')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
plt.title("Elbow Method for Drop-off Locations")
plt.grid()
plt.savefig("dropoff_elbow_method.png")
# plt.show()

repo_path = os.path.expanduser("~/Desktop/MyUberData")
map_path = os.path.join(repo_path, "uber_clusters_map.html")

optimal_k = 4  

pickup_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
uber_data["pickup_cluster"] = pickup_kmeans.fit_predict(uber_data[['begintrip_lat', 'begintrip_lng']])

dropoff_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
uber_data["dropoff_cluster"] = dropoff_kmeans.fit_predict(uber_data[['dropoff_lat', 'dropoff_lng']])

map_clusters = folium.Map(location=[uber_data['begintrip_lat'].mean(), uber_data['begintrip_lng'].mean()], zoom_start=5)

bounds = [
    [uber_data["begintrip_lat"].min(), uber_data["begintrip_lng"].min()],
    [uber_data["begintrip_lat"].max(), uber_data["begintrip_lng"].max()],
    [uber_data["dropoff_lat"].min(), uber_data["dropoff_lng"].min()],
    [uber_data["dropoff_lat"].max(), uber_data["dropoff_lng"].max()]
]

map_clusters.fit_bounds(bounds)

pickup_cluster_group = folium.FeatureGroup(name="Pickup Clusters", overlay=True)
dropoff_cluster_group = folium.FeatureGroup(name="Dropoff Clusters", overlay=True)

pickup_cluster = MarkerCluster(name="Pickup Cluster Markers", disableClusteringAtZoom=6).add_to(pickup_cluster_group)
for _, row in uber_data.iterrows():
    pickup_popup = folium.Popup(f"""
        <div style="width: 350px; font-size: 16px;">
            <b>Pickup Address:</b> {row['begintrip_address']}<br>
            <b>Cluster:</b> {row['pickup_cluster']}
        </div>
    """, max_width=450)

    folium.CircleMarker(
        location=[row["begintrip_lat"], row["begintrip_lng"]],
        radius=3,
        color="blue",
        fill=True,
        fill_opacity=0.8,
        popup=pickup_popup
    ).add_to(pickup_cluster)

dropoff_cluster = MarkerCluster(name="Dropoff Cluster Markers", disableClusteringAtZoom=6).add_to(dropoff_cluster_group)
for _, row in uber_data.iterrows():
    dropoff_popup = folium.Popup(f"""
        <div style="width: 350px; font-size: 16px;">
            <b>Drop-off Address:</b> {row['dropoff_address']}<br>
            <b>Cluster:</b> {row['dropoff_cluster']}
        </div>
    """, max_width=450)

    folium.CircleMarker(
        location=[row["dropoff_lat"], row["dropoff_lng"]],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.8,
        popup=dropoff_popup
    ).add_to(dropoff_cluster)

map_clusters.add_child(pickup_cluster_group)
map_clusters.add_child(dropoff_cluster_group)

folium.LayerControl().add_to(map_clusters)

map_clusters.save(map_path)

print("✅ Separate Uber cluster map saved at:", map_path)

print("## 📌 K-Means Clustering Insights\n")
print(f"- Used **4 Clusters** for pickup locations\n")

this_map = folium.Map(prefer_canvas=True)

trip_bounds = [
    [uber_data["begintrip_lat"].min(), uber_data["begintrip_lng"].min()],
    [uber_data["begintrip_lat"].max(), uber_data["begintrip_lng"].max()],
    [uber_data["dropoff_lat"].min(), uber_data["dropoff_lng"].min()],
    [uber_data["dropoff_lat"].max(), uber_data["dropoff_lng"].max()]
]

this_map.fit_bounds(trip_bounds)

def plotDot(uber_data):
    pickup_time = uber_data.trip_start_time.strftime('%Y-%m-%d %I:%M %p')
    dropoff_time = uber_data.trip_end_time.strftime('%Y-%m-%d %I:%M %p')

    pickup_popup = folium.Popup(f"""
        <div style="width: 350px; font-size: 16px;">
            <b>Pickup Date & Time:</b> {pickup_time}<br>
            <b>Pickup Address:</b> {uber_data.begintrip_address}
        </div>
    """, max_width=450)

    dropoff_popup = folium.Popup(f"""
        <div style="width: 350px; font-size: 16px;">
            <b>Dropoff Date & Time:</b> {dropoff_time}<br>
            <b>Address:</b> {uber_data.dropoff_address}
        </div>
    """, max_width=450)

    folium.CircleMarker(location=[uber_data.begintrip_lat, uber_data.begintrip_lng], radius=3, color="blue", weight=5, popup=pickup_popup, tooltip="Pickup Location").add_to(this_map)
    folium.CircleMarker(location=[uber_data.dropoff_lat, uber_data.dropoff_lng], radius=3, color="red", weight=5, popup=dropoff_popup, tooltip="Dropoff Location").add_to(this_map)
    folium.PolyLine(locations=[(uber_data.begintrip_lat, uber_data.begintrip_lng), (uber_data.dropoff_lat, uber_data.dropoff_lng)], color="green", weight=2, tooltip="Trip Path").add_to(this_map)

uber_data.apply(plotDot, axis=1)
map_path = os.path.join(repo_path, "myubermap.html")
this_map.save(map_path)

print("## 🗺️ Interactive Uber Map\n")
print(f"🔗 [Click here to view my Uber trip map](https://paulgarces.github.io/MyUberData/myubermap.html)\n")

sys.stdout.close()
sys.stdout = sys.__stdout__

print(f"Report saved to: {report_path}")
print(f"Map saved to: {map_path}")