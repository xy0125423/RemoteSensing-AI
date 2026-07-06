import rasterio
import numpy as np
import matplotlib.pyplot as plt

with rasterio.open("data/raw/sentinel2_sample.tif") as dataset:

    # =============================
    # Read RGB Bands
    # =============================
    b2 = dataset.read(1).astype("float32")
    b3 = dataset.read(2).astype("float32")
    b4 = dataset.read(3).astype("float32")

    # =============================
    # Stack RGB
    # =============================
    rgb = np.stack([b4, b3, b2], axis=-1)

    # =============================
    # 2%~98% Stretch
    # =============================
    low = np.percentile(rgb, 2)
    high = np.percentile(rgb, 98)

    rgb_clip = np.clip(rgb, low, high)
    rgb_norm = (rgb_clip - low) / (high - low)

    # =============================
    # Display Image
    # =============================
    bounds = dataset.bounds
    plt.imshow(rgb_norm, extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
    plt.title("Sentinel-2 True Color")
    plt.show()