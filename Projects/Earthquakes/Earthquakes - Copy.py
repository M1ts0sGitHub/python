import requests
import pandas as pd
from datetime import datetime, timedelta
import folium
from folium.plugins import FloatImage, HeatMap
import time
from sklearn.cluster import KMeans
import numpy as np
import random

url = "http://www.geophysics.geol.uoa.gr/stations/gmaps3/event_output2j.php?type=cat"
response = requests.get(url)

df_list = []
# Split the response into columns and rows
line_split = response.text.split('\n')
for line in line_split:
    word_split = line.split()
    df_list.append(word_split)
df = pd.DataFrame(df_list[1:], columns=df_list[0])
df = df.iloc[:500]

# Convert Lat & Long from text to float
df['Lat'] = df['Lat'].str.replace(',', '.').astype(float)
df['Long'] = df['Long'].str.replace(',', '.').astype(float)
df['Dep'] = df['Dep'].str.replace(',', '.').astype(float)
df['Mag'] = df['Mag'].str.replace(',', '.').astype(float)

# Create one date&time column from Year, Mo, Dy, Hr, Mn
df['Datetime'] = df['Year'].astype(str) + '-' + df['Mo'].astype(str) + '-' + df['Dy'].astype(str) + ' ' + df['Hr'].astype(str) + ':' + df['Mn'].astype(str)

# Clean up the dataframe
cols_to_drop = ['RMS', 'dx', 'dy', 'dz', 'Np', 'Na', 'Gap', 'Year', 'Mo', 'Dy', 'Hr', 'Mn', 'Sec']
df.drop(cols_to_drop, axis=1, inplace=True)

df = df.iloc[::-1]

# Extract the coordinates for clustering
coords = df[['Lat', 'Long']]

# Define the grid
grid_size = 0.5  # Size of the grid cells

# Calculate the number of cells in the grid
lat_bins = np.arange(df['Lat'].min(), df['Lat'].max(), grid_size)
long_bins = np.arange(df['Long'].min(), df['Long'].max(), grid_size)

# Create the 2D histogram
hist, xedges, yedges = np.histogram2d(df['Lat'], df['Long'], bins=[lat_bins, long_bins])

# Find the centers of the high-density cells
xidx, yidx = np.where(hist > np.percentile(hist, 95))  # Use the top 5% densest cells
cluster_centers = np.array([(xedges[i] + xedges[i+1]) / 2 for i in xidx]), np.array([(yedges[i] + yedges[i+1]) / 2 for i in yidx])

# Perform K-Means clustering using the high-density cell centers as initial centers
initial_centers = np.column_stack(cluster_centers)
kmeans = KMeans(n_clusters=len(initial_centers), init=initial_centers, n_init=1).fit(coords)
df['Cluster'] = kmeans.labels_

# Generate random colors for clusters
random.seed(42)
colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(initial_centers))]

# Create a map centered around the mean latitude and longitude of the data
m = folium.Map(location=[df['Lat'].mean(), df['Long'].mean()], zoom_start=7)

# Define a function to determine marker color based on cluster
def get_cluster_color(cluster):
    return colors[cluster]

# Add the heatmap overlay
heat_data = [[row['Lat'], row['Long']] for index, row in df.iterrows()]
HeatMap(heat_data, radius=15).add_to(m)

# Loop over each row in the dataframe
for index, row in df.iterrows():
    # Calculate the size of the marker based on magnitude
    size = 0.5 + row['Mag'] * 1.3
    # Determine the color of the marker based on cluster
    color = get_cluster_color(row['Cluster'])

    popup_text = f" Date: {row['Datetime']} <br> Magnitude: {row['Mag']:.1f} <br> Depth: {row['Dep']:.1f} <br> Cluster: {row['Cluster']}"
    iframe = folium.IFrame(popup_text, width=190, height=85)
    popup = folium.Popup(iframe, max_width=190)

    # Add a circle marker to the map
    folium.CircleMarker(
        location=[row['Lat'], row['Long']],
        radius=size,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=1,
        popup=popup).add_to(m)

photo = 'https://dl3.pushbulletusercontent.com/zVp8ThIqafF2GKXnYnW3qNgSJ4F4cRmS/image.png'
FloatImage(photo, top=0, left=0).add_to(m)

# Generate the legend dynamically
legend_html = '<div style="position: fixed; top: 10px; right: 10px; width: 150px; height: auto; border:2px solid grey; z-index:9999; font-size:14px; background-color: white;">&nbsp; <b>Cluster Legend</b> <br>'
for i in range(len(initial_centers)):
    legend_html += f'&nbsp; Cluster {i} &nbsp; <i class="fa fa-circle fa-1x" style="color:{colors[i]}"></i><br>'
legend_html += '</div>'

m.get_root().html.add_child(folium.Element(legend_html))

# Save the map as an HTML file
m.save('earthquakes.html')
time.sleep(20)
