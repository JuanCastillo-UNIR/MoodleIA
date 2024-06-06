from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
import logging, os


class GptFAQs:
    _openai_service: OpenAIService
    _prompt_service: PromptService

    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService):
        self._openai_service = openai_service
        self._prompt_service = prompt_service

    def get_faqs_azure(self, content:str):
        logging.info(f"get_schema_content input question={content}") 
        prompt = self._prompt_service.load_sys_prompt_from_file(
                os.path.join(os.path.join('src/api/workflows/FAQs/prompt.json'))
        )
        output = self._openai_service.call_api(
            prompt=prompt,
            user_msg=content
        )
        return output