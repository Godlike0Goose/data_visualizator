from typing import Optional

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


class ModelsSupportedParams:
    """
    Определяет поддерживаемые параметры для каждой модели.
    Использует имена полей из ModelParams как единый источник истины.
    """

    Lasso_model = set(ALL_PARAMS.keys()) - {
        AllParamNames.l1_ratio,
        AllParamNames.solver,
    }
    Elastic_Net_model = set(ALL_PARAMS.keys()) - {AllParamNames.solver}
    Ridge_model = set(ALL_PARAMS.keys()) - {
        AllParamNames.l1_ratio,
        AllParamNames.selection,
    }

    @classmethod
    def get_params_for_model(cls, model_name: str) -> set:
        """Возвращает множество поддерживаемых параметров для указанной модели."""
        return getattr(cls, model_name, set())
