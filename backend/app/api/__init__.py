from .customers import router as customers_router
from .auditors import router as auditors_router
from .workflow import router as workflow_router

__all__ = [
    "customers_router",
    "auditors_router", 
    "workflow_router"
]
