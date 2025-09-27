from typing import Optional


ALL_PARAMS: dict[str, type] = {
    "alpha": Optional[float],
    "random_state": Optional[int],
    "copy_X": Optional[bool],
    "selection": Optional[str],
    "l1_ratio": Optional[float],
    "fit_intercept": Optional[bool],
    "tol": Optional[float],
    "solver": Optional[str],
    "max_iter": Optional[int],
    "positive": Optional[bool],
}


class ModelsSupportedParams:
    """
    Определяет поддерживаемые параметры для каждой модели.
    Использует имена полей из ModelParams как единый источник истины.
    """

    Lasso_model = set(ALL_PARAMS.keys()) - {"l1_ratio", "solver"}
    Elastic_Net_model = set(ALL_PARAMS.keys()) - {"solver"}
    Ridge_model = set(ALL_PARAMS.keys()) - {"l1_ratio", "selection"}

    @classmethod
    def get_params_for_model(cls, model_name: str) -> set:
        """Возвращает множество поддерживаемых параметров для указанной модели."""
        return getattr(cls, model_name, set())
