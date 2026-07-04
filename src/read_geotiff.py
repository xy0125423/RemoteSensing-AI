import rasterio

with rasterio.open("data/raw/sentinel2_sample.tif") as dataset:
    #===========================
    #GeoTIFF Metadata
    #===========================
    print("GeoTIFF Metadata")
    print("CRS:",dataset.crs)
    print("Bounds:",dataset.bounds)
    print("Transform:",dataset.transform)
    print("Width:",dataset.width)
    print("Height:",dataset.height)
    print("Band Count:",dataset.count)
    print("Datatype:",dataset.dtypes)
    print("Band Descriptions:",dataset.descriptions)

    print()
    #=====================================
    #Read  Bands
    #=====================================
    b4 = dataset.read(3).astype('float32')  # Red
    b8 = dataset.read(4).astype('float32')  # NIR

    #=====================================
    #B4 Information
    #=====================================
    print("B4(Red) ")
    print("Min:", b4.min())
    print("Max:", b4.max())
    print("Mean:", b4.mean())
    print("Std:", b4.std())
    print("Shape:", b4.shape)
    print("Data Type:", b4.dtype)
    print("Type:", type(b4))

    print()

    #=====================================
    #B8 Information
    #=====================================
    print("B8(NIR) ")
    print("Min:", b8.min())
    print("Max:", b8.max())
    print("Mean:", b8.mean())
    print("Std:", b8.std())
    print("Shape:", b8.shape)
    print("Data Type:", b8.dtype)
    print("Type:", type(b8))

    ndvi = (b8 - b4) / (b8 + b4)
    print("NDVI ")
    print("Min:", ndvi.min())
    print("Max:", ndvi.max())
    print("Mean:", ndvi.mean())
    print("Std:", ndvi.std())
    print("Shape:", ndvi.shape)
    print("Data Type:", ndvi.dtype)
    print("Type:", type(ndvi))
