import requests
import pandas as pd
from datetime import datetime, timedelta
import folium
from folium.plugins import FloatImage
import time

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

# convert Lat & Long from text to int
df['Lat'] = df['Lat'].str.replace(',', '.').astype(float)
df['Long'] = df['Long'].str.replace(',', '.').astype(float)
df['Dep'] = df['Dep'].str.replace(',', '.').astype(float)
df['Mag'] = df['Mag'].str.replace(',', '.').astype(float)

# Create one date&time column from Year, Mo, Dy, Hr, Mn
df['Datetime']=df['Year'].astype(str) + '-' + df['Mo'].astype(str) + '-' + df['Dy'].astype(str) + ' ' + df['Hr'].astype(str) + ':' + df['Mn'].astype(str)

# Clean up the dataframe
cols_to_drop = ['RMS','dx','dy','dz','Np','Na','Gap','Year', 'Mo', 'Dy', 'Hr', 'Mn', 'Sec']
df.drop(cols_to_drop, axis=1, inplace=True)

print(df.head(10))
df = df.iloc[::-1]

# Create a map centered around the mean latitude and longitude of the data
m = folium.Map(location=[df['Lat'].mean(), df['Long'].mean()], zoom_start=7)

# Define a function to determine marker color based on date
def get_color(date):
    today = datetime.today()
    if date.date() == today.date():
        return 'red'   # Today
    elif date >= today - timedelta(days=7):
        return 'orange'  # Last 7 days
    else:
        return 'green'  # Last 30 days

# Loop over each row in the dataframe
for index, row in df.iterrows():
    # Calculate the size of the marker based on magnitude
    size = 0.5 + row['Mag'] * 1.3
    # Determine the color of the marker based on date
    color = get_color(pd.to_datetime(row['Datetime']))

    popup_text = f" Date: {row['Datetime']} <br> Magnitude: {row['Mag']:.1f} <br> Deapth: {row['Dep']:.1f}"
    iframe = folium.IFrame(popup_text, width=190, height=75)
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


legend_html = '''
     <div style="position: fixed;
                 top: 10px; right: 10px; width: 130px; height: 90px;
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color: white;">&nbsp; <b>Color Legend</b> <br>
                 &nbsp; Today &nbsp; <i class="fa fa-circle fa-1x" style="color:red"></i><br>
                 &nbsp; Last 7 days &nbsp; <i class="fa fa-circle fa-1x" style="color:orange"></i><br>
                 &nbsp; Last 30 days &nbsp; <i class="fa fa-circle fa-1x" style="color:green"></i>
      </div>
     '''

m.get_root().html.add_child(folium.Element(legend_html))

# Save the map as an HTML file
m.save('earthquakes.html')
time.sleep(20)