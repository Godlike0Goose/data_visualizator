from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class ModelParams:
    """
    A data class to store parameters for machine learning models.
    Only non-None parameters will be used when passed to a model.
    """

    alpha: Optional[float] = None  # [0, inf)
    l1_ratio: Optional[float] = None
    fit_intercept: Optional[bool] = None
    max_iter: Optional[int] = None
    tol: Optional[float] = None
    solver: Optional[str] = None
    positive: Optional[bool] = None
    copy_X: Optional[bool] = None
    random_state: Optional[int] = None
    selection: Optional[str] = None

    def set_param(self, param: str, value):
        """Sets a parameter and returns its new value."""
        setattr(self, param, value)
        return getattr(self, param, None)

    def to_dict(self) -> dict:
        """
        Converts the parameters to a dictionary, excluding None values.
        This is useful for passing parameters to scikit-learn models.
        """
        return {k: v for k, v in asdict(self).items() if v is not None}
