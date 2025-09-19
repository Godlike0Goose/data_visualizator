import logging
import pandas as pd

logger = logging.getLogger(__name__)


def get_features(df: pd.DataFrame, target_var: str | None) -> list[str]:
    """Возвращает список признаков (все столбцы, кроме целевой переменной).

    Args:
        df (pd.DataFrame): DataFrame с данными.
        target_var (str | None): Имя целевой переменной.

    Returns:
        list[str]: Список имен столбцов-признаков.
    """
    if target_var is None or target_var not in df.columns:
        return []
    return [col for col in df.columns if col != target_var]


def validate_and_update_cell(
    df: pd.DataFrame, row: int, col: int, value: str
) -> bool:
    """Проверяет и обновляет значение в ячейке DataFrame.

    Выполняет валидацию типа данных перед обновлением.

    Args:
        df (pd.DataFrame): DataFrame для обновления.
        row (int): Индекс строки.
        col (int): Индекс столбца.
        value (str): Новое значение в виде строки.

    Returns:
        bool: True, если обновление прошло успешно, иначе False.
    """
    column_dtype = df.iloc[:, col].dtype
    original_value = df.iat[row, col]

    try:
        if pd.api.types.is_numeric_dtype(column_dtype):
            if pd.api.types.is_integer_dtype(column_dtype):
                new_value = int(value)
            else:
                new_value = float(value)
        elif pd.api.types.is_string_dtype(column_dtype) or pd.api.types.is_object_dtype(
            column_dtype
        ):
            if value.isnumeric() or (value.replace(".", "", 1).isdigit()):
                raise ValueError(
                    f"Attempted to enter a numeric value '{value}' into a string column."
                )
            new_value = value
        else:
            new_value = value 

        df.iloc[row, col] = new_value
        return True

    except (ValueError, TypeError) as e:
        logger.warning("Validation failed for column '%s': %s. Reverting to original value '%s'.", df.columns[col], e, original_value)
        df.iloc[row, col] = original_value
        return False