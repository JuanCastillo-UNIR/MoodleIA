from api.common.services.openai_service import OpenAIService
from api.common.services.prompt_service import PromptService
from api.workflows.FAQs.gpt_faqs import GptFAQs


class FAQsWorkflow:
    _openai_service: GptFAQs
    
    def __init__(self,
        openai_service: OpenAIService, 
        prompt_service: PromptService
    ) -> None:
        self._openai_service = GptFAQs(openai_service, prompt_service)

    def execute(self, request: str, faqs:str) -> str: 
        if request.lower()=='asesor': 
            import time; time.sleep(1)
            return f'<h2>Dirígete al siguiente número de Whatsapp: <a href="https://web.whatsapp.com/send?phone=34689909323&text=%C2%A1Hola!%20Quiero%20m%C3%A1s%20informaci%C3%B3n%20sobre...">Contacta con un asesor.</a></h2>'
        request = {'Pregunta': request, 'FAQs': faqs}  
        return self._openai_service.get_faqs_azure(str(request))