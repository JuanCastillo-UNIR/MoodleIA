from api.common.dependency_container import DependencyContainer
from fastapi import APIRouter, Response


router = APIRouter(prefix="/contenidos", tags=["contenidos"])

@router.post("/get_FAQs")
async def generate_FAQs(pregunta: str, FAQs: str) -> Response:
    return DependencyContainer.get_faqs_workflow().execute(pregunta, FAQs)
