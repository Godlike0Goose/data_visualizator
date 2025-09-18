import pandas as pd
from pathlib import Path


def read_dataset_from_Path(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    elif suffix in [".xls", ".xlsx"]:
        return pd.read_excel(path)
    elif suffix == ".json":
        return pd.read_json(path)
    elif suffix == ".parquet":
        return pd.read_parquet(path)
    elif suffix == ".feather":
        return pd.read_feather(path)
    elif suffix in [".h5", ".hdf5"]:
        return pd.read_hdf(path)
    elif suffix == ".pkl":
        return pd.read_pickle(path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")
