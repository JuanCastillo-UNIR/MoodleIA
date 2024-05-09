from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.contenidos_azure.request_content import SchemaRequest
from src.api.workflows.contenidos_azure.gpt_content import GptContent


class ContentWorkflow:
    _openai_service: GptContent
    
    def __init__(self,
        openai_service: OpenAIService, 
        prompt_service: PromptService
    ) -> None:
        self._openai_service = GptContent(openai_service, prompt_service)

    def execute(self, request: SchemaRequest) -> dict: # type: ignore
        return self._openai_service.get_schema_content(str(request))