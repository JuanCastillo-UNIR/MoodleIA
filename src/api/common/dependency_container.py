import json
import logging
from logging import Logger

from api.workflows.FAQs.faqs_workflow import FAQsWorkflow
from fastapi.security import OAuth2PasswordBearer
from openai import AzureOpenAI, OpenAI

from api.common.services.openai_service import OpenAIService
from api.common.services.prompt_service import PromptService
from common.application_settings import ApplicationSettings
from domain.entities.general_llm_information import (
    GeneralLLMInformation,
    ModelInformation,
)


class DependencyContainer:
    _LOGGER_NAME = "logger"
    _oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    _application_settings: ApplicationSettings
    _openai_service: OpenAIService
    _azure_openai_service: OpenAIService
    _prompt_service: PromptService
    _prompt_service: PromptService

    @classmethod
    def initialize(cls) -> None:
        cls._initialize_application_settings()
        cls._initialize_azure_openai_service()
        cls._initialize_openai_service()
        cls._initialize_prompt_service()

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls._application_settings

    @classmethod
    def get_openai_engine(cls) -> OpenAI:
        return OpenAI(
            api_key=cls._application_settings.OPEN_AI__API_KEY,
        )

    @classmethod
    def get_azure_openai_engine(cls) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=cls._application_settings.OPEN_AI__API_KEY,
            api_version=cls._application_settings.OPEN_AI__API_VERSION,
            azure_endpoint=cls._application_settings.OPEN_AI__AZURE_ENDPOINT,
        )

    @classmethod
    def get_azure_embedding_engine(cls) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=cls._application_settings.OPEN_AI_EMBEDDINGS__API_KEY,
            api_version=cls._application_settings.OPEN_AI_EMBEDDINGS__API_VERSION,
            azure_endpoint=cls._application_settings.OPEN_AI_EMBEDDINGS__AZURE_ENDPOINT,
        )

    @classmethod
    def get_openai_embedding_engine(cls) -> OpenAI:
        return OpenAI(
            api_key=cls._application_settings.OPEN_AI__OAI_API_KEY,
        )

    @classmethod
    def get_azure_openai_service(cls) -> OpenAIService:
        return cls._azure_openai_service

    @classmethod
    def get_openai_service(cls) -> OpenAIService:
        return cls._openai_service

    @classmethod
    def get_prompt_service(cls) -> PromptService:
        return cls._prompt_service

    @classmethod
    def get_llm_information(cls) -> GeneralLLMInformation:
        heavy_dict: dict[str, str] = json.loads(
            cls._application_settings.LLM__INFORMATION_HEAVY
        )
        light_dict: dict[str, str] = json.loads(
            cls._application_settings.LLM__INFORMATION_LIGHT
        )
        heavy: ModelInformation = ModelInformation(**heavy_dict)
        light: ModelInformation = ModelInformation(**light_dict)
        return GeneralLLMInformation(heavy=heavy, light=light)

    @classmethod
    def get_logger(cls) -> Logger:
        logger = logging.getLogger(cls._LOGGER_NAME)
        return logger

    @classmethod
    def _initialize_application_settings(cls) -> None:
        cls._application_settings = ApplicationSettings()  # type: ignore

    @classmethod
    def _initialize_openai_service(cls) -> None:
        cls._openai_service = OpenAIService(
            logger=cls.get_logger(),
            openai_client=cls.get_openai_engine(),
        )

    @classmethod
    def _initialize_azure_openai_service(cls) -> None:
        cls._azure_openai_service = OpenAIService(
            logger=cls.get_logger(),
            openai_client=cls.get_azure_openai_engine(),
        )

    @classmethod
    def _initialize_prompt_service(cls) -> None:
        cls._prompt_service = PromptService(
            logger=cls.get_logger(),
        )

    @classmethod
    def faqs_workflow(cls) -> FAQsWorkflow:
        logging.info("Creating SchemaWorkflow with dependencies")
        return FAQsWorkflow(
            cls.get_openai_service(),
            cls.get_prompt_service(),
        )