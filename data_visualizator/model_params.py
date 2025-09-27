from copy import deepcopy
from trycast import isassignable

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

    __slots__ = list(ALL_PARAMS.keys())
    __annotations__ = ALL_PARAMS

    def __init__(self, **kwargs):
        for param, expected_type in self.__annotations__.items():
            value = kwargs.get(param, None)

            if value is not None and not isassignable(value, expected_type):
                raise TypeError(
                    f"Parameter '{param}' must be of type {expected_type}, got {type(value)}"
                )

            setattr(self, param, value)

        for key in kwargs:
            if key not in self.__annotations__:
                raise ValueError(f"Unknown parameter '{key}' for ModelParams")

    def __repr__(self):
        params = ", ".join(
            f"{param}={getattr(self, param)!r}" for param in self.__annotations__
        )
        return f"{self.__class__.__name__}({params})"

    def __eq__(self, other):
        if not isinstance(other, ModelParams):
            return False
        return all(
            getattr(self, param) == getattr(other, param)
            for param in self.__annotations__
        )

    def copy(self):
        """Возвращает глубокую копию объекта."""
        return deepcopy(self)
