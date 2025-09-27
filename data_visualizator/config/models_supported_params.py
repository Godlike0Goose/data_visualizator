from typing import Optional
from enum import Enum

from .base_config import AllParamNames


ALL_PARAMS: dict[str, type] = {
    AllParamNames.alpha: Optional[float],
    AllParamNames.random_state: Optional[int],
    AllParamNames.copy_X: Optional[bool],
    AllParamNames.selection: Optional[str],
    AllParamNames.l1_ratio: Optional[float],
    AllParamNames.fit_intercept: Optional[bool],
    AllParamNames.tol: Optional[float],
    AllParamNames.solver: Optional[str],
    AllParamNames.max_iter: Optional[int],
    AllParamNames.positive: Optional[bool],
}


class ModelsSupportedParams(Enum):
    """
    Определяет поддерживаемые параметры для каждой модели.
    Использует имена полей из ModelParams как единый источник истины.
    """

    Lasso_model = {
        AllParamNames.alpha,
        AllParamNames.fit_intercept,
        AllParamNames.copy_X,
        AllParamNames.max_iter,
        AllParamNames.tol,
        AllParamNames.positive,
        AllParamNames.random_state,
        AllParamNames.selection,
    }

    ElasticNet_model = {
        AllParamNames.alpha,
        AllParamNames.l1_ratio,
        AllParamNames.fit_intercept,
        AllParamNames.copy_X,
        AllParamNames.max_iter,
        AllParamNames.tol,
        AllParamNames.positive,
        AllParamNames.random_state,
        AllParamNames.selection,
    }

    Ridge_model = {
        AllParamNames.alpha,
        AllParamNames.fit_intercept,
        AllParamNames.copy_X,
        AllParamNames.max_iter,
        AllParamNames.tol,
        AllParamNames.solver,
        AllParamNames.positive,
        AllParamNames.random_state,
    }

    @classmethod
    def get_params_for_model(cls, model_name: str) -> set:
        """Возвращает множество поддерживаемых параметров для указанной модели."""
        return getattr(cls, model_name, set())
