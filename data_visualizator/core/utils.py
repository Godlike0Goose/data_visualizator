import pandas as pd
from pathlib import Path


def read_dataset_from_path(file_path, **kwargs):
    """Читает набор данных из файла по указанному пути.

    Поддерживает различные форматы файлов, включая CSV, Excel, JSON, Parquet,
    Feather, HDF5 и Pickle. Позволяет передавать дополнительные именованные
    аргументы (`**kwargs`) в соответствующую функцию чтения pandas.

    Args:
        file_path (str или Path): Путь к файлу с набором данных.
        **kwargs: Дополнительные именованные аргументы, которые будут переданы
            в соответствующую функцию чтения pandas (`read_csv`, `read_excel` и т.д.).

    Returns:
        pd.DataFrame: Загруженный набор данных в виде DataFrame.

    Examples:
        Чтение CSV с разделителем ';':
        >>> read_dataset_from_path('data.csv', sep=';')

        Чтение определенного листа из файла Excel:
        >>> read_dataset_from_path('data.xlsx', sheet_name='Sales')

        Чтение CSV без строки заголовка:
        >>> read_dataset_from_path('data.csv', header=None)

    Raises:
        FileNotFoundError: Если файл по указанному пути не найден.
        ValueError: Если формат файла не поддерживается.
        Любые другие исключения, которые могут быть вызваны соответствующими
        функциями pandas `read_*`.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path, **kwargs)
    elif suffix in [".xls", ".xlsx"]:
        return pd.read_excel(path, **kwargs)
    elif suffix == ".json":
        return pd.read_json(path, **kwargs)
    elif suffix == ".parquet":
        return pd.read_parquet(path, **kwargs)
    elif suffix == ".feather":
        return pd.read_feather(path, **kwargs)
    elif suffix in [".h5", ".hdf5"]:
        return pd.read_hdf(path, **kwargs)
    elif suffix == ".pkl":
        return pd.read_pickle(path, **kwargs)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")
    
def save_dataframe_to_path(df, path, **kwargs):
    """Сохраняет DataFrame в файл по указанному пути.

    Функция автоматически определяет формат файла по его расширению и использует
    соответствующий метод pandas для сохранения. Поддерживает передачу
    дополнительных именованных аргументов (`**kwargs`) в эти методы.

    Args:
        df (pd.DataFrame): DataFrame, который нужно сохранить.
        path (str или Path): Путь к файлу для сохранения.
        **kwargs: Дополнительные именованные аргументы, которые будут переданы
            в соответствующий метод сохранения pandas (`to_csv`, `to_excel` и т.д.).

    Examples:
        Сохранение в CSV без индекса и с разделителем ';':
        >>> save_dataframe_to_path(df, 'data.csv', index=False, sep=';')

        Сохранение в Excel на определенный лист:
        >>> save_dataframe_to_path(df, 'data.xlsx', index=False, sheet_name='Отчет')

        Сохранение в "красивый" JSON с отступами:
        >>> save_dataframe_to_path(df, 'data.json', orient='records', indent=4)

    Raises:
        ValueError: Если формат файла (расширение) не поддерживается.
        Любые другие исключения, которые могут быть вызваны соответствующими
        методами pandas `to_*` (например, `PermissionError`, если файл занят).

    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return df.to_csv(path, **kwargs)
    elif suffix in [".xls", ".xlsx"]:
        return df.to_excel(path, **kwargs)
    elif suffix == ".json":
        return df.to_json(path, **kwargs)
    elif suffix == ".parquet":
        return df.to_parquet(path, **kwargs)
    elif suffix == ".feather":
        return df.to_feather(path, **kwargs)
    elif suffix in [".h5", ".hdf5"]:
        return df.to_hdf(path, key="df", mode="w", **kwargs)
    elif suffix == ".pkl":
        return df.to_pickle(path, **kwargs)
 