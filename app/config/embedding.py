from config.settings import SETTINGS
from config.constants import EMBEDDING_MODEL_PROVIDERS


match SETTINGS.EMBEDDING_PROVIDER.lower():
    case EMBEDDING_MODEL_PROVIDERS.OPENAI:
        from langchain_openai import OpenAIEmbeddings

        embedding = OpenAIEmbeddings(
            model=SETTINGS.EMBEDDING_MODEL, api_key=SETTINGS.EMBEDDING_PROVIDER_API_KEY
        )

    case EMBEDDING_MODEL_PROVIDERS.HUGGINGFACE:
        from langchain_huggingface import HuggingFaceEmbeddings

        embedding = HuggingFaceEmbeddings(model_name=SETTINGS.EMBEDDING_MODEL)

    case EMBEDDING_MODEL_PROVIDERS.GOOGLE:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embedding = GoogleGenerativeAIEmbeddings(
            model=SETTINGS.EMBEDDING_MODEL,
            google_api_key=SETTINGS.EMBEDDING_PROVIDER_API_KEY,
        )

    case _:
        from langchain_huggingface import HuggingFaceEmbeddings

        model_kwargs = {"device": "cpu"}
        embedding = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", model_kwargs=model_kwargs
        )
