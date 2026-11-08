from support_agent.settings import Settings


def test_settings_load_azure_openai_values_from_env_file(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "AZURE_OPENAI_API_KEY=test-key\n"
        "AZURE_OPENAI_ENDPOINT=https://example.openai.azure.com/\n"
        "AZURE_OPENAI_DEPLOYMENT_NAME=test-deployment\n"
        "OPENAI_API_VERSION=2025-03-01-preview\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.azure_openai_api_key == "test-key"
    assert settings.azure_openai_endpoint == "https://example.openai.azure.com/"
    assert settings.azure_openai_deployment_name == "test-deployment"
    assert settings.openai_api_version == "2025-03-01-preview"
