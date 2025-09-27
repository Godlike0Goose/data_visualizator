import pandas as pd


class DatasetFilter:
    def __init__(self, df):
        self._df = df

    def Delite_empty_data(self):
        """передается dataframe который преобразуется в dataframe
        без строк с пустыми значениями"""
        df_clean = self.df.dropna()
        return df_clean

    def One_hot_encoding(self, df):
        """использует метод OHE для преобразования
         котегориальных переменныв некотегорельные
        путем преобразования тех самы котегориальных
            значений в колонки с данными 1 и 0"""
        categorical_cols = df.select_dtypes(exclude=["number", "bool"]).columns.tolist()
        if not categorical_cols:
            return df.copy()
        df_encoded = pd.get_dummies(
            df, columns=categorical_cols, drop_first=False, dtype=int
        )
        return df_encoded
