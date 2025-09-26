from enum import Enum

class ModelsSupportedParams:

    class LassoModel(Enum):
        alpha = "alpha"
        fit_intercept = "fit_intercept"
        copy_X = "copy_X"
        max_iter = "max_iter"
        tol = "tol"
        positive = "positive"
        random_state = "random_state"
        selection = "selection"

    class ElasticNetModel(Enum):
        alpha = "alpha"
        fit_intercept = "fit_intercept"
        copy_X = "copy_X"
        max_iter = "max_iter"
        tol = "tol"
        positive = "positive"
        random_state = "random_state"
        selection = "selection"
        l1_ratio = "l1_ratio"

    class Ridge(Enum):
        alpha = "alpha"
        fit_intercept = "fit_intercept"
        copy_X = "copy_X"
        max_iter = "max_iter"
        tol = "tol"
        positive = "positive"
        random_state = "random_state"
        solver = "solver"