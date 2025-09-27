from enum import Enum

from sklearn.linear_model import Ridge, Lasso, ElasticNet


class SupportedModels(Enum):
    Ridge_model = Ridge
    Lasso_model = Lasso
    ElasticNet_model = ElasticNet
