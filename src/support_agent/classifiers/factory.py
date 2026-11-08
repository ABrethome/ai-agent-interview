from langchain.chat_models import init_chat_model
from langchain_openai import AzureChatOpenAI

from support_agent.classifiers.base import Classifier
from support_agent.classifiers.keyword import KeywordClassifier
from support_agent.classifiers.llm import LlmClassifier
from support_agent.settings import Settings


def create_classifier(settings: Settings) -> Classifier:
    if settings.classifier_provider == "keyword":
        return KeywordClassifier()

    if settings.model_name is None:
        raise ValueError(
            "MODEL_NAME must be set when CLASSIFIER_PROVIDER is 'llm'"
        )

    if settings.model_name.startswith("azure_openai:"):
        azure_settings = {
            "AZURE_OPENAI_API_KEY": settings.azure_openai_api_key,
            "AZURE_OPENAI_ENDPOINT": settings.azure_openai_endpoint,
            "AZURE_OPENAI_DEPLOYMENT_NAME": settings.azure_openai_deployment_name,
            "OPENAI_API_VERSION": settings.openai_api_version,
        }
        missing_settings = [
            name for name, value in azure_settings.items() if not value
        ]
        if missing_settings:
            raise ValueError(
                "Missing Azure OpenAI settings: " + ", ".join(missing_settings)
            )

        return LlmClassifier(
            AzureChatOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.openai_api_version,
                azure_deployment=settings.azure_openai_deployment_name,
            )
        )

    return LlmClassifier(init_chat_model(settings.model_name))
