from config.settings import SETTINGS
from config.constants import EMBEDDING_MODEL_PROVIDERS


match SETTINGS.EMBEDDING_MODEL_PROVIDER.lower():
    case EMBEDDING_MODEL_PROVIDERS.OPENAI:
        # WARNING: NEED TO HANDLE API KEY ALSO
        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(model=SETTINGS.EMBEDDING_MODEL)

    case EMBEDDING_MODEL_PROVIDERS.HUGGINGFACE:
        # WARNING: NEED TO HANDLE API KEY ALSO
        from langchain_huggingface import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(model_name=SETTINGS.EMBEDDING_MODEL)

    case EMBEDDING_MODEL_PROVIDERS.GEMINI:
        # WARNING: NEED TO HANDLE API KEY ALSO
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(model=SETTINGS.EMBEDDING_MODEL)

    case _:
        from langchain_huggingface import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
