import logging
from logging import Logger
from openai import AzureOpenAI
from src.api.workflows.Foros.foros_workflow import ForosWorkflow
from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.FAQs.workflow_faqs import FAQsWorkflow
from src.common.application_settings import ApplicationSettings
from src.api.common.services.llm import LLM
from sqlmodel import create_engine
from sqlalchemy import Engine

class DependencyContainer:
    _LOGGER_NAME = "logger"
    _azure_openai_client: AzureOpenAI
    _application_settings: ApplicationSettings
    _database_engine: Engine
    _openai_service: OpenAIService
    _prompt_service: PromptService
    _llm: LLM

    @classmethod
    def initialize(cls) -> None:
        cls._initialize_application_settings()
        cls._initialize_database_engine()
        cls._initialize_openai_service()
        cls._initialize_prompt_service()
        cls._initialize_llm_manager()

    @classmethod
    def get_logger(cls) -> Logger:
        return logging.getLogger(cls._LOGGER_NAME)

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls._application_settings

    @classmethod
    def _initialize_llm_manager(cls) -> None:
        cls._llm = LLM()

    @classmethod
    def get_llm_manager(cls) -> LLM:
        return cls._llm

    @classmethod
    def _initialize_application_settings(cls) -> None:
        cls._application_settings = ApplicationSettings()

    @classmethod
    def get_database_engine(cls) -> Engine:
        return cls._database_engine

    @classmethod
    def _initialize_database_engine(cls) -> None:
        cls._database_engine = create_engine(
            f"sqlite:///src/domain/moodle.db", echo=False
        )

    @classmethod
    def _initialize_openai_service(cls) -> None:
        cls._openai_service = OpenAIService(
            logger=cls.get_logger(),
            openai_client=cls.get_azure_openai_client(),
        )

    @classmethod
    def get_azure_openai_client(cls) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=cls._application_settings.OPEN_AI__API_KEY,
            api_version=cls._application_settings.OPEN_AI__API_VERSION,
            azure_endpoint=cls._application_settings.OPEN_AI__AZURE_ENDPOINT,
        )

    @classmethod
    def _initialize_prompt_service(cls) -> None:
        cls._prompt_service = PromptService(
            logger=cls.get_logger(),
            sql_engine=cls.get_database_engine(),
        )

    @classmethod
    def get_openai_service(cls) -> OpenAIService:
        return cls._openai_service

    @classmethod
    def get_prompt_service(cls) -> PromptService:
        return cls._prompt_service

    @classmethod
    def get_faqs_workflow(cls) -> FAQsWorkflow:
        logging.info("Creating FAQsWorkflow with dependencies")
        return FAQsWorkflow(
            cls.get_openai_service(),
            cls.get_prompt_service(),
        )

    @classmethod
    def get_foros_workflow(cls) -> ForosWorkflow:
        logging.info("Creating ForosWorkflow with dependencies")
        return ForosWorkflow(
            cls.get_openai_service(),
            cls.get_prompt_service(),
        )