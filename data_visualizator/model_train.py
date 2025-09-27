from typing import Optional


from .config import SupportedModels
from .model_params import ModelParams
from .utils import get_params_for_model




class ModelTrainer:
    def __init__(self, model: Optional[SupportedModels] = None, params: Optional[ModelParams] = None):
        self.set_model(model)
        self.set_params(params)

    def set_model(self, model: Optional[SupportedModels]):
        if model is None:
            self.model = None
            self.needed_params = set()
            return

        if not isinstance(model, SupportedModels):
            raise TypeError("Model must be of type SupportedModels or None")
        
        self.model = model
        self.needed_params = get_params_for_model(self.model)
    
    def set_params(self, params: Optional[ModelParams]):
        if params is None:
            self.params = None
            return
        
        if not isinstance(params, ModelParams):
            raise TypeError("Params must be of type ModelParams or None")
        
        self.params = params
    
    def train(self, X, y):
        if self.model is None:
            raise ValueError("Model is not set")
        
        if self.params is None:
            raise ValueError("Params are not set")
        
        actual_params = {
            param: getattr(self.params, param)
            for param in self.needed_params
            if getattr(self.params, param) is not None
        }
        
        model_class = self.model.value
        model_instance = model_class(**actual_params)
        
        model_instance.fit(X, y)
        
        return model_instance