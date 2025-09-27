from enum import StrEnum


class SupportedModels(StrEnum):
    Ridge_model = "Ridge"
    Lasso_model = "Lasso"
    Elastic_Net_model = "ElasticNet"


class AllParamNames(StrEnum):
    alpha = "alpha"
    random_state = "random_state"
    copy_X = "copy_X"
    selection = "selection"
    l1_ratio = "l1_ratio"
    fit_intercept = "fit_intercept"
    tol = "tol"
    solver = "solver"
    max_iter = "max_iter"
    positive = "positive"
