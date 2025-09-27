from pathlib import Path
import pandas as pd
from .config import AllParamNames, SupportedModels, ModelsSupportedParams

def get_params_for_model(model: SupportedModels) -> set:
    """Возвращает множество поддерживаемых параметров для указанной модели."""

    if not isinstance(model, SupportedModels):
        raise TypeError("Model must be of type SupportedModels")

    model_name = model.name
    return ModelsSupportedParams[model_name].value

def read_data_file(file_path: str):
    '''проверяет тип файла и открывает его
     так же обрабатывает отсутстве файла по данному пути 
     и вариацию поддерживаемого фала для pandas  '''
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

