import pandas as pd
from pathlib import Path


def read_dataset_from_Path(file_path):
    """Читает набор данных из файла по указанному пути.

    Поддерживает различные форматы файлов, включая CSV, Excel, JSON, Parquet,
    Feather, HDF5 и Pickle.

    Args:
        file_path (str или Path): Путь к файлу с набором данных.

    Returns:
        pd.DataFrame: Загруженный набор данных в виде DataFrame.

    Raises:
        FileNotFoundError: Если файл по указанному пути не найден.
        ValueError: Если формат файла не поддерживается.
    """
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
