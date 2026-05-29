import json
import csv
from collections import defaultdict

input_file = "Streetlights.geojson"
output_file = "streetlight_type_grid_small.csv"

GRID_SIZE = 0.1

counts = defaultdict(int)
watts_sum = defaultdict(float)
watts_count = defaultdict(int)

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

for feature in features:
    props = feature.get("properties", {})
    geom = feature.get("geometry", {})

    if geom.get("type") != "Point":
        continue

    coords = geom.get("coordinates", [])
    if len(coords) < 2:
        continue

    try:
        lon = float(coords[0])
        lat = float(coords[1])
    except:
        continue

    if not (110 <= lon <= 155 and -45 <= lat <= -5):
        continue

    bulb_type = props.get("bulb_type", "Unknown")
    bulb_watts = props.get("bulb_watts", "")

    if bulb_type is None or str(bulb_type).strip() == "":
        bulb_type = "Unknown"
    else:
        bulb_type = str(bulb_type).strip()

    try:
        bulb_watts = float(bulb_watts)
    except:
        bulb_watts = None

    lat_bin = round(round(lat / GRID_SIZE) * GRID_SIZE, 1)
    lon_bin = round(round(lon / GRID_SIZE) * GRID_SIZE, 1)

    key = (lat_bin, lon_bin, bulb_type)

    counts[key] += 1

    if bulb_watts is not None:
        watts_sum[key] += bulb_watts
        watts_count[key] += 1

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "lat_bin",
        "lon_bin",
        "bulb_type",
        "streetlight_count",
        "avg_bulb_watts"
    ])

    for (lat_bin, lon_bin, bulb_type), count in sorted(counts.items()):
        if watts_count[(lat_bin, lon_bin, bulb_type)] > 0:
            avg_watts = watts_sum[(lat_bin, lon_bin, bulb_type)] / watts_count[(lat_bin, lon_bin, bulb_type)]
        else:
            avg_watts = ""

        writer.writerow([
            lat_bin,
            lon_bin,
            bulb_type,
            count,
            avg_watts
        ])

print(f"Done. Created {output_file}")
print(f"Original features: {len(features)}")
print(f"Reduced rows: {len(counts)}")