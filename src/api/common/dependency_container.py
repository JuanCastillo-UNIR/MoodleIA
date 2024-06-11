import logging, json
from logging import Logger
from openai import AzureOpenAI, OpenAI
from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.FAQs.workflow_faqs import FAQsWorkflow
from src.api.workflows.Foros.workflow_content import ForosWorkflow
from src.common.application_settings import ApplicationSettings
# from src.api.common.services.observability import Observability
from src.api.common.services.llm import LLM
from sqlmodel import create_engine
from sqlalchemy import Engine
from src.domain.entities.general_llm_information import (
    GeneralLLMInformation,
    ModelInformation,
)

class DependencyContainer:
    _LOGGER_NAME = "logger"
    # _oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    _application_settings: ApplicationSettings
    _database_engine: Engine
    _openai_service: OpenAIService
    _azure_openai_service: OpenAIService
    # _qdrant_service: QdrantService
    _prompt_service: PromptService
    _prompt_service: PromptService
    # _google_service: GoogleService

    @classmethod
    def initialize(cls) -> None:
        cls._initialize_application_settings()
        # cls._initialize_application_insights()
        cls._initialize_database_engine()
        cls._initialize_azure_openai_service()
        cls._initialize_openai_service()
        cls._initialize_prompt_service()
        # cls._initialize_qdrant_service()
        # cls._initialize_google_service()
        # cls._initialize_observability()
        # cls._initialize_llm_manager()
    
    @classmethod
    def get_logger(cls) -> Logger:
        logger = logging.getLogger(cls._LOGGER_NAME)
        return logger

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls._application_settings

    @classmethod
    def _initialize_llm_manager(cls) -> LLM:
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
    def get_openai_engine(cls) -> OpenAI:
        return OpenAI(
            api_key=cls._application_settings.OPEN_AI__OAI_API_KEY,
        )
    
    @classmethod
    def get_azure_openai_engine(cls) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=cls._application_settings.OPEN_AI__API_KEY,
            api_version=cls._application_settings.OPEN_AI__API_VERSION,
            azure_endpoint=cls._application_settings.OPEN_AI__AZURE_ENDPOINT,
        )

    @classmethod
    def _initialize_database_engine(cls) -> None:
        cls._database_engine = create_engine(f"sqlite:///src/domain/moodle.db", echo=False) 
        # url = f"mssql+pyodbc://{cls._application_settings.SQL_SERVER__USERNAME}:{cls._application_settings.SQL_SERVER__PASSWORD}@{cls._application_settings.SQL_SERVER__HOST}:{cls._application_settings.SQL_SERVER__PORT}/{cls._application_settings.SQL_SERVER__NAME}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
        # cls._database_engine = create_engine(url=url, echo=False)
    
    @classmethod
    def _initialize_azure_openai_service(cls) -> None:
        cls._azure_openai_service = OpenAIService(
            logger=cls.get_logger(),
            openai_client=cls.get_azure_openai_engine(),
        )
    
    @classmethod
    def _initialize_openai_service(cls) -> None:
        cls._openai_service = OpenAIService(
            logger=cls.get_logger(),
            openai_client=cls.get_openai_engine(),
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
    def get_faqs_workflow(cls) -> FAQsWorkflow:
        logging.info("Creating SchemaWorkflow with dependencies")
        return FAQsWorkflow(
            cls.get_openai_service(),
            cls.get_prompt_service(),
        )

    @classmethod
    def get_foros_content(cls) -> ForosWorkflow:
        logging.info("Creating SchemaWorkflow with dependencies")
        return ForosWorkflow(
            cls.get_openai_service(),
            cls.get_prompt_service(),
        ) 
    
    # @classmethod
    # def _initialize_observability(cls) -> None:
    #     settings = cls._application_settings
    #     _observability = Observability(port = settings.PHOENIX_PORT).set_observability()