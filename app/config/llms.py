from config.settings import SETTINGS
from config.constants import LLM_MODEL_PROVIDERS

llm = None

match SETTINGS.LLM_PROVIDER.lower():
    case LLM_MODEL_PROVIDERS.GOOGLE:
        from langchain_google_genai import ChatGoogleGenerativeAI

        # TODO: need to configure each parameter to be dynamic.
        llm = ChatGoogleGenerativeAI(
            model=SETTINGS.LLM_MODEL,
            google_api_key=SETTINGS.LLM_PROVIDER_API_KEY,
            timeout=None,
            temperature=0,
            max_tokens=None,
            max_retries=2,
        )

    case LLM_MODEL_PROVIDERS.GROQ:
        from langchain_groq import ChatGroq

        llm = ChatGroq(
            model=SETTINGS.LLM_MODEL,
            api_key=SETTINGS.LLM_PROVIDER_API_KEY,
            temperature=0,
            max_tokens=None,
            max_retries=2,
        )

    case LLM_MODEL_PROVIDERS.ANTHROPIC:
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(
            model=SETTINGS.LLM_MODEL,
            api_key=SETTINGS.LLM_PROVIDER_API_KEY,
            temperature=0,
            max_tokens=None,
            max_retries=2,
        )

    case LLM_MODEL_PROVIDERS.OPENAI:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=SETTINGS.LLM_MODEL,
            api_key=SETTINGS.LLM_PROVIDER_API_KEY,
            temperature=0,
            max_tokens=None,
            max_retries=2,
        )

    case _:
        raise ValueError(f"Unsupported LLM provider: {SETTINGS.LLM_PROVIDER}")
