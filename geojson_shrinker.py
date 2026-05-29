import json
import math
from random import randint

# ---------------------------------------------------------
# Haversine distance in kilometres
# ---------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return 2 * R * math.asin(math.sqrt(a))

# ---------------------------------------------------------
# Load your data
# ---------------------------------------------------------
with open("AUS_tiny.json", "r") as f:
    data = json.load(f)

# ---------------------------------------------------------
# Thinning radius (km)
# Increase this to remove more points
# ---------------------------------------------------------
radius_km = 30

filtered = []
print(len(data))
x = 0
while len(filtered) < 10000 and x < 100000:
    point = data[randint(0, len(data)-1)]
    lat, lon = point["lat"], point["lon"]
    
    too_close = False
    x+=1
    for kept in filtered:
        if haversine(lat, lon, kept["lat"], kept["lon"]) < radius_km:
            too_close = True
            break

    if not too_close:
        filtered.append(point)
        x += 1
        if x % 10 == 0:
            print(f"Processed {x} points.")
    

# ---------------------------------------------------------
# Save the thinned dataset
# ---------------------------------------------------------
with open("AUS_thinned.json", "w") as f:
    json.dump(filtered, f, separators=(",", ":"))

print(f"Done. Reduced from {len(data)} to {len(filtered)} points.")
