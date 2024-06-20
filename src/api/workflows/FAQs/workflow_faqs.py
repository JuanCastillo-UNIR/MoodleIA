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
        request = {'Pregunta': request, 'FAQs': faqs}  
        response = self._openai_service.get_faqs_azure(str(request))
        faq = max(response['FAQs'], key=lambda x: float(x['Score']))
        if float(faq['Score']) >= 7: content = f"<h2>{faq['FAQ']}</h2>{faq['Contenido']}" 
        if 4 < float(faq['Score']) < 7: 
            content = f"""
                        <h2>{faq['FAQ']}</h2>{faq['Contenido']}
                        <h2>Si esta FAQ no se ajusta a tu pregunta, puedes dirigirte al siguiente número de Whatsapp: <a href="https://web.whatsapp.com/send?phone=34689909323">Contacta con un asesor.</a></h2>
            """
        if float(faq['Score']) <= 4: content = f'<h2>No encontramos ninguna FAQ relacionada a la pregunta. Dirígete al siguiente número de Whatsapp: <a href="https://web.whatsapp.com/send?phone=34689909323">contacta con un asesor.</a></h2>'
        return content
      