"""
Hands-on Lab: Interactive Visual Analytics with Folium
=======================================================

SpaceX Falcon 9 First Stage Landing Prediction
Analyzing launch site locations using interactive Folium maps.

Tasks:
  1. Mark all launch sites on a map
  2. Mark the success/failed launches for each site on the map
  3. Calculate the distances between a launch site and its proximities

Output files (all prefixed with 'lab_jupyter_launch_site_location.'):
  - lab_jupyter_launch_site_location.task1_launch_sites.html
  - lab_jupyter_launch_site_location.task2_launch_outcomes.html
  - lab_jupyter_launch_site_location.task3_proximity_distances.html
"""

import subprocess
import sys

# Install dependencies if needed
subprocess.check_call([sys.executable, "-m", "pip", "install", "folium", "pandas", "-q"])

import io
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians

# ---------------------------------------------------------------------------
# Output file prefix
# ---------------------------------------------------------------------------
PREFIX = "lab_jupyter_launch_site_location."


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

print("Loading SpaceX launch geo data...")
URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud"
    "/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
)
response = requests.get(URL)
spacex_df = pd.read_csv(io.BytesIO(response.content))

# Keep relevant columns
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]

# One row per launch site (first occurrence gives the representative coordinate)
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

print("Launch sites:")
print(launch_sites_df.to_string(index=False))
print()


# ---------------------------------------------------------------------------
# TASK 1: Mark all launch sites on a map
# ---------------------------------------------------------------------------
print("Task 1: Marking launch sites on map...")

# Start centered at NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# NASA JSC reference marker
circle = folium.Circle(
    nasa_coordinate,
    radius=1000,
    color='#d35400',
    fill=True
).add_child(folium.Popup('NASA Johnson Space Center'))

marker = folium.Marker(
    nasa_coordinate,
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12px; color:#d35400;"><b>NASA JSC</b></div>'
    )
)
site_map.add_child(circle)
site_map.add_child(marker)

# Add a circle and label for every launch site
map_center = [launch_sites_df['Lat'].mean(), launch_sites_df['Long'].mean()]
map_site = folium.Map(location=map_center, zoom_start=4)

for _, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    label = row['Launch Site']

    folium.Circle(
        coordinate,
        radius=1000,
        color='#d35400',
        fill=True,
        fill_opacity=0.6
    ).add_to(map_site)

    folium.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12px; color:#d35400;"><b>%s</b></div>' % label
        )
    ).add_to(map_site)

output_task1 = PREFIX + "task1_launch_sites.html"
map_site.save(output_task1)
print(f"  Saved: {output_task1}")


# ---------------------------------------------------------------------------
# TASK 2: Mark success/failed launches for each site on the map
# ---------------------------------------------------------------------------
print("Task 2: Marking launch outcomes on map...")

map_outcomes = folium.Map(location=map_center, zoom_start=4)

# Separate clusters for successes and failures
cluster_success = MarkerCluster(name="Class = 1 (Success)")
cluster_failure = MarkerCluster(name="Class = 0 (Failure)")

for _, row in spacex_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    cls = row['class']
    color = 'green' if cls == 1 else 'red'
    popup_html = (
        f"<b>Launch Site:</b> {row['Launch Site']}<br>"
        f"<b>Class:</b> {cls}"
    )

    folium.CircleMarker(
        location=coordinate,
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=250)
    ).add_to(cluster_success if cls == 1 else cluster_failure)

cluster_success.add_to(map_outcomes)
cluster_failure.add_to(map_outcomes)
folium.LayerControl(collapsed=False).add_to(map_outcomes)

output_task2 = PREFIX + "task2_launch_outcomes.html"
map_outcomes.save(output_task2)
print(f"  Saved: {output_task2}")


# ---------------------------------------------------------------------------
# TASK 3: Calculate distances between a launch site and its proximities
# ---------------------------------------------------------------------------
print("Task 3: Calculating proximity distances and mapping...")


def calculate_distance(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points in km (Haversine formula)."""
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def add_connection(map_obj, origin, dest, dest_name, line_color="#000000"):
    """Add a destination marker, polyline, and distance label to the map."""
    dist_km = calculate_distance(origin[0], origin[1], dest[0], dest[1])
    dist_mi = dist_km * 0.621371
    distance_text = f"{dest_name}: {dist_km:.2f} km ({dist_mi:.2f} mi)"
    midpoint = [(origin[0] + dest[0]) / 2, (origin[1] + dest[1]) / 2]

    # Destination marker
    folium.Marker(dest, popup=dest_name).add_to(map_obj)

    # Connecting line with popup and tooltip
    line = folium.PolyLine(
        locations=[origin, dest],
        weight=4,
        opacity=0.9,
        color=line_color
    ).add_to(map_obj)
    line.add_child(folium.Popup(distance_text, max_width=300))
    line.add_child(folium.Tooltip(distance_text))

    # Midpoint distance label
    folium.Marker(
        location=midpoint,
        icon=folium.DivIcon(
            html=(
                f'<div style="font-size:12px; font-weight:bold; color:{line_color};">'
                f'{distance_text}</div>'
            )
        )
    ).add_to(map_obj)

    print(f"  {distance_text}")


# Example: proximity from a launch site near Houston
launch_coord   = [29.56062, -95.08324]   # launch site
railroad_coord = [29.53971, -95.12066]   # nearest railroad
city_coord     = [29.50535, -95.09148]   # nearest city (League City)
coast_coord    = [29.56159, -95.07298]   # nearest coastline

# Also compute the coastline distance for the Florida sites
launch_lat_fl = 28.56367
launch_lon_fl = -80.57163
coast_lat_fl  = 28.56234   # approx. nearest coastline for CCAFS
coast_lon_fl  = -80.56799
dist_coastline_fl = calculate_distance(launch_lat_fl, launch_lon_fl, coast_lat_fl, coast_lon_fl)
print(f"  CCAFS to nearest coastline: {dist_coastline_fl:.2f} km")

# Build the proximity map
map_proximity = folium.Map(location=launch_coord, zoom_start=11)

# Add MousePosition plugin so coordinates appear on hover
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
map_proximity.add_child(mouse_position)

# Launch site marker
folium.Marker(launch_coord, popup="Launch Site").add_to(map_proximity)

# Draw connections to each nearby feature
add_connection(map_proximity, launch_coord, railroad_coord,
               "Nearest Railroad", line_color="#2c3e50")
add_connection(map_proximity, launch_coord, city_coord,
               "Nearest City - League City", line_color="#27ae60")
add_connection(map_proximity, launch_coord, coast_coord,
               "Nearest Coastline", line_color="#2980b9")

output_task3 = PREFIX + "task3_proximity_distances.html"
map_proximity.save(output_task3)
print(f"  Saved: {output_task3}")

print("\nDone. Open the HTML files in a browser to view the interactive maps.")
