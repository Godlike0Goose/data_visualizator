from .config import AllParamNames, SupportedModels, ModelsSupportedParams

def get_params_for_model(model: SupportedModels) -> set:
    """Возвращает множество поддерживаемых параметров для указанной модели."""

    if not isinstance(model, SupportedModels):
        raise TypeError("Model must be of type SupportedModels")

    model_name = model.name
    return ModelsSupportedParams[model_name].value