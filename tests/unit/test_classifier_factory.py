from unittest.mock import Mock, patch

import pytest

from support_agent.classifiers.factory import create_classifier
from support_agent.settings import Settings


def test_create_classifier_passes_settings_to_azure_model() -> None:
    settings = Settings(
        classifier_provider="llm",
        model_name="azure_openai:gpt-5-mini",
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://example.openai.azure.com/",
        azure_openai_deployment_name="test-deployment",
        openai_api_version="2025-03-01-preview",
        _env_file=None,
    )

    with patch(
        "support_agent.classifiers.factory.AzureChatOpenAI"
    ) as azure_chat_openai:
        create_classifier(settings)

    azure_chat_openai.assert_called_once_with(
        api_key="test-key",
        azure_endpoint="https://example.openai.azure.com/",
        api_version="2025-03-01-preview",
        azure_deployment="test-deployment",
        temperature=0,
    )


def test_create_classifier_reports_missing_azure_settings() -> None:
    settings = Settings(
        classifier_provider="llm",
        model_name="azure_openai:gpt-5-mini",
        _env_file=None,
    )

    with pytest.raises(ValueError, match="Missing Azure OpenAI settings"):
        create_classifier(settings)


def test_create_classifier_does_not_pass_azure_settings_for_other_provider() -> None:
    settings = Settings(
        classifier_provider="llm",
        model_name="openai:gpt-5-mini",
        _env_file=None,
    )

    with patch(
        "support_agent.classifiers.factory.init_chat_model",
        return_value=Mock(),
    ) as init_chat_model:
        create_classifier(settings)

    init_chat_model.assert_called_once_with(
        "openai:gpt-5-mini",
        temperature=0,
    )
