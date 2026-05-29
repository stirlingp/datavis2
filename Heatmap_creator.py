import json
import numpy as np
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Load your AUS_thinned.json (lat, lon, mpsas)
# ---------------------------------------------------------
with open("AUS_thinned.json", "r") as f:
    data = json.load(f)

lats = np.array([d["lat"] for d in data])
lons = np.array([d["lon"] for d in data])
mpsas = np.array([d["mpsas"] for d in data])

# ---------------------------------------------------------
# 2. Create a grid covering Australia
# ---------------------------------------------------------
lat_min, lat_max = -48, -6
lon_min, lon_max = 108, 158

grid_res = 500  # increase for smoother output

grid_lon, grid_lat = np.meshgrid(
    np.linspace(lon_min, lon_max, grid_res),
    np.linspace(lat_min, lat_max, grid_res)
)

# ---------------------------------------------------------
# 3. Interpolate using Radial Basis Function
# ---------------------------------------------------------
rbf = Rbf(lons, lats, mpsas, function="linear")
grid_mpsas = rbf(grid_lon, grid_lat)

# ---------------------------------------------------------
# 4. Save as a PNG heatmap (transparent background)
# ---------------------------------------------------------
plt.figure(figsize=(6, 8))
plt.imshow(
    grid_mpsas,
    extent=[lon_min, lon_max, lat_min, lat_max],
    origin="lower",
    cmap="gnuplot2_r",
    alpha=0.95
)
plt.axis("off")
plt.savefig("luminance_heatmap.png", dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
plt.close()

print("Created luminance_heatmap.png")
