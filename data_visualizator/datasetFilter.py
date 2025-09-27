import pandas as pd


class DatasetFilter:
    @staticmethod
    def remove_empty_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Удаляет строки, содержащие хотя бы одно пустое (NaN) значение.
        и возвращает  без строк с пропущенными значениями.
        """
        return df.dropna()

    @staticmethod
    def one_hot_encoding(df: pd.DataFrame) -> pd.DataFrame:
        """использует метод OHE для преобразования
         котегориальных переменныв некотегорельные
        путем преобразования тех самы котегориальных
            значений в колонки с данными 1 и 0"""
        categorical_cols = df.select_dtypes(exclude=["number", "bool"]).columns.tolist()
        
        if not categorical_cols:
            return df.copy()
        
        return pd.get_dummies(
            df,
            columns=categorical_cols,
            drop_first=False,
            dtype=int
        )
