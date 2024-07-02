from api.common.services.openai_service import OpenAIService
from api.common.services.prompt_service import PromptService
from api.workflows.FAQs.faqs_gpt import GptFAQs


class FAQsWorkflow:
    _openai_service: GptFAQs
    
    def __init__(self,
        openai_service: OpenAIService, 
        prompt_service: PromptService
    ) -> None:
        self._openai_service = GptFAQs(openai_service, prompt_service)

    def get_FAQs(self) -> str: 
        from api.workflows.FAQs.faqs_extract import FAQsExtract
        return FAQsExtract().FAQs

    def IA_FAQs(self, pregunta: str, faqs:str) -> str: 
        return self._openai_service.get_faqs_azure(str(
            {'Pregunta': pregunta, 
             'FAQs': faqs}  
        ))