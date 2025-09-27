from dataclasses import make_dataclass, field

from .config.models_supported_params import ALL_PARAMS


class ModelParams:
    """
    Класс для хранения параметров модели с их типами.

    Атрибуты:
        alpha (Optional[float]): Параметр регуляризации.
        random_state (Optional[int]): Случайное зерно для воспроизводимости.
        copy_X (Optional[bool]): Флаг копирования входных данных перед обработкой.
        selection (Optional[str]): Метод выбора признаков.
        l1_ratio (Optional[float]): Соотношение L1/L2 для ElasticNet.
        fit_intercept (Optional[bool]): Флаг вычисления свободного члена.
        tol (Optional[float]): Допустимая точность сходимости.
        solver (Optional[str]): Алгоритм оптимизации.
        max_iter (Optional[int]): Максимальное количество итераций.
        positive (Optional[bool]): Флаг, разрешающий только положительные коэффициенты.
    """

    __slots__ = [ALL_PARAMS.keys()]
    __annotations__ = ALL_PARAMS

    def __init__(self):
        for param in ALL_PARAMS.keys():
            setattr(self, param, None)
