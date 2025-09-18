import pandas as pd
def read_dataset_from_Path (path):
    ds = pd.read_csv(path)
    return ds
