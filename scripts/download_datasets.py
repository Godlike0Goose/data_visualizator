from kaggle import api
import os

datasets = ["zynicide/wine-reviews", "heptapod/diabetes-data"]
os.makedirs("kaggle_data", exist_ok=True)

for ds in datasets:
    outdir = os.path.join("kaggle_data", ds.replace("/", "_"))
    os.makedirs(outdir, exist_ok=True)
    print("Downloading", ds, "->", outdir)
    api.dataset_download_files(ds, path=outdir, unzip=True, quiet=False)
