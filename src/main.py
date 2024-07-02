from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.common.dependency_container import DependencyContainer
from api.exception_middleware import ExceptionMiddleware
from api.workflows.health_checks import health_check_router
from api.workflows import FAQs_router
DependencyContainer.initialize()


if not __name__.startswith("__mp"):
    app = FastAPI(
        title="Chatbot FAQs Becat", version="1.0.0", 
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ExceptionMiddleware)
    app.include_router(health_check_router.router)
    app.include_router(FAQs_router.router)