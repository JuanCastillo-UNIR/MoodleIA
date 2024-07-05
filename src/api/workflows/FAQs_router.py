from api.common.dependency_container import DependencyContainer
from api.workflows.FAQs.faqs_request import FAQsRequest
from fastapi import APIRouter, Response


router = APIRouter(prefix="/FAQs", tags=["FAQs"])

@router.get("/get_FAQs")
async def get_FAQs() -> Response:
    return DependencyContainer.faqs_workflow().get_FAQs()

@router.get("/IA_FAQs")
async def IA_FAQs(request: FAQsRequest) -> Response:
    return DependencyContainer.faqs_workflow().IA_FAQs(request.pregunta, request.FAQs)