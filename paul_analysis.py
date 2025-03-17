import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import folium
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', None)

# Load the data
uber_data = pd.read_csv("/Users/paulgarces/Desktop/uber_data/Rider/trips_data-0.csv")
uber_data.head(5)

if __name__ == "__main__":
    print(uber_data.head())

print(uber_data.isna().sum())
uber_data.dropna(inplace=True)

# convert the date columns to datetime
uber_data['trip_start_time'] = pd.to_datetime(uber_data['begin_trip_time'])
uber_data['trip_end_time'] = pd.to_datetime(uber_data['dropoff_time'])
uber_data['request_time'] = pd.to_datetime(uber_data['request_time'])


uber_data['hour'] = uber_data['trip_start_time'].dt.hour
uber_data['day_of_week'] = uber_data['trip_start_time'].dt.day_name()
uber_data['month'] = uber_data['trip_start_time'].dt.month_name()
uber_data['trip_duration'] = (uber_data['trip_end_time'] - uber_data['trip_start_time']).dt.total_seconds() / 60

print("Top 10 Pickup Locations:")
print(uber_data['begintrip_address'].value_counts().head(10))

print("-------------------")

print("Top 10 Dropoff Locations:")
print(uber_data['dropoff_address'].value_counts().head(10))

print("Total Trips:", len(uber_data))
print("Average Trip Duration (minutes):", uber_data['trip_duration'].mean())
print("Longest Trip Duration (minutes):", uber_data['trip_duration'].max())
print("Shortest Trip Duration (minutes):", uber_data['trip_duration'].min())
print("Earliest Trip:", uber_data['trip_start_time'].min())
print("Latest Trip:", uber_data['trip_end_time'].max())

# plt.figure(figsize=(8,5))
# sns.histplot(uber_data['trip_duration'], bins=30)
# plt.xlabel("Trip Duration (minutes)")
# plt.ylabel("Number of Trips")
# plt.title("Distribution of Uber Trip Durations")
# plt.show()

# plt.figure(figsize=(10,5))
# sns.countplot(x='hour', data=uber_data)
# plt.title("Uber Trips by Hour of the Day")
# plt.xlabel("Hour of the Day")
# plt.ylabel("Number of Trips")
# plt.show()

# plt.figure(figsize=(10,5))
# sns.countplot(x='day_of_week', data=uber_data, order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
# plt.title("Uber Trips by Day of the Week")
# plt.xlabel("Day of the Week")
# plt.ylabel("Number of Trips")
# plt.show()

pickup_coords = uber_data[['begintrip_lat', 'begintrip_lng']]

# K-Means clustering
pickup_coords = uber_data[['begintrip_lat', 'begintrip_lng']]

wcss = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pickup_coords)
    wcss.append(kmeans.inertia_)

#Elbow Method plot
# plt.figure(figsize=(8,5))
# plt.plot(k_values, wcss, linestyle='-')
# plt.xlabel("Number of Clusters (k)")
# plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
# plt.title("Elbow Method for Optimal k")
# plt.show()

pickup_coords = uber_data[["begintrip_lat", "begintrip_lng"]]

# Actual K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=370)
uber_data["pickup_cluster"] = kmeans.fit_predict(pickup_coords)

# Showing the clusters
# plt.figure(figsize=(8,6))
# sns.scatterplot(data=uber_data, x="begintrip_lng", y="begintrip_lat", hue="pickup_cluster")
# plt.title("Clustering Uber Pickup Locations")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.legend(title="Cluster")
# plt.show()

regular_trips = folium.FeatureGroup(name="Regular Uber Trips")
clustered_trips = folium.FeatureGroup(name="Clustered Pickup Locations")

#making a folium map
this_map = folium.Map(prefer_canvas=True)

def plotDot(uber_data):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''

    pickup_time = uber_data.trip_start_time.strftime('%Y-%m-%d %I:%M %p')
    dropoff_time = uber_data.trip_end_time.strftime('%Y-%m-%d %I:%M %p')

    pickup_popup = folium.Popup(
        f"""
        <div style="width: 220px; font-size: 14px;">
            <b>Pickup Date & Time:</b> {pickup_time}<br>
            <b>Address:</b> {uber_data.begintrip_address}
        </div>
        """, max_width=300
    )

    dropoff_popup = folium.Popup(
        f"""
        <div style="width: 220px; font-size: 14px;">
            <b>Dropoff Date & Time:</b> {dropoff_time}<br>
            <b>Address:</b> {uber_data.dropoff_address}
        </div>
        """, max_width=300
    )

    folium.CircleMarker(location=[uber_data.begintrip_lat, uber_data.begintrip_lng],
                        radius=2,
                        color = "blue",
                        weight=5,
                        popup= pickup_popup,
                        tooltip="Pickup Location").add_to(this_map)
    
    folium.CircleMarker(location=[uber_data.dropoff_lat, uber_data.dropoff_lng],
                        radius=2,
                        color = "red",
                        weight=5,
                        popup= dropoff_popup,
                        tooltip="Dropoff Location").add_to(this_map)
    
    folium.PolyLine(
        locations=[(uber_data.begintrip_lat, uber_data.begintrip_lng), 
                   (uber_data.dropoff_lat, uber_data.dropoff_lng)],
        color="green",
        weight=2,
        tooltip="Trip Path"
    ).add_to(this_map)


#use df.apply(,axis=1) to "iterate" through every row in your dataframe
uber_data.apply(plotDot, axis = 1)


this_map.fit_bounds(this_map.get_bounds())

save_path = '/Users/paulgarces/Desktop/Desktop - Paul’s MacBook Pro/myubermap.html'
this_map.save(save_path)

print(uber_data.dtypes)

## Using ML to predict the fare amound based on features

# One-Hot Encoding for categorical features (product_type, day_of_week, city)
df_pandas_encoded = pd.get_dummies(uber_data, columns=["product_type", "day_of_week", "city"], drop_first=True)
encoder = OneHotEncoder(sparse_output=False)
one_hot_encoded = encoder.fit_transform(uber_data[["product_type","day_of_week","city"]])
encoded_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(["product_type","day_of_week","city"]))
concact_df = pd.concat([uber_data, encoded_df], axis=1)

dropped_df = concact_df.drop(["begintrip_address", "dropoff_address", "trip_start_time", "trip_end_time", "request_time", "begintrip_lat", "begintrip_lng", "dropoff_lat", "dropoff_lng", "pickup_cluster", "day_of_week", 
                     "dropoff_time", "status", "begin_trip_time", "city", "product_type", "fare_currency", "hour", "month"], axis=1)

X = dropped_df[['distance', 'trip_duration', 'product_type_Comfort', 'product_type_uberX', 'product_type_uberXL', 'product_type_uberx', 'day_of_week_Friday', 'day_of_week_Monday', 'day_of_week_Saturday', 
                'day_of_week_Sunday', 'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday', 'city_Madrid', 'city_Mexico City', 'city_NYC Suburbs', 'city_New York City', 
                'city_Quito', 'city_Seattle']]
y = dropped_df[['fare_amount']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lm = LinearRegression()
lm.fit(X_train, y_train)
lm_predictions = lm.predict(X_test)