from .auto_budget import *
from .task_budget import *

budgets = {
    AutoBudget.slug: AutoBudget,
    TaskBudget.slug: TaskBudget,
}

__all__ = [
    'AutoBudget',
    'TaskBudget',
]
