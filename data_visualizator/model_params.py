from typing import Optional

class ModelParams:
    def __init__(
            self,
            alpha: Optional[float] = None,                  # [0, inf)
            l1_ratio: Optional[float] = None,
            fit_intercept: Optional[bool] = None,         
            max_iter: Optional[int] = None,               
            tol: Optional[float] = None,
            solver: Optional[str] = None,
            positive: Optional[bool] = None,
            copy_X: Optional[bool] = None,
            random_state: Optional[int] = None,
            selection: Optional[str] = None
    ):
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.solver = solver
        self.positive = positive
        self.copy_X = copy_X
        self.random_state = random_state
        self.selection = selection
        
    def set_param(self, param: str, value):
        setattr(self, param, value)
        return getattr(self, param, None)