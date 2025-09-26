# from langfuse.callback import CallbackHandler

from config.settings import SETTINGS

####################################
# LANGFUSE HANDLER
####################################


def get_all_callbacks(session_id: str) -> list:
    callbacks = []
    # if all(
    #     [
    #         SETTINGS.LANGFUSE_HOST,
    #         SETTINGS.LANGFUSE_PUBLIC_KEY,
    #         SETTINGS.LANGFUSE_SECRET_KEY,
    #     ]
    # ):
    #     # https://langfuse.com/docs/integrations/langchain/example-python-langgraph
    #     langfuse_handler = CallbackHandler(
    #         host=SETTINGS.LANGFUSE_HOST,
    #         public_key=SETTINGS.LANGFUSE_PUBLIC_KEY,
    #         secret_key=SETTINGS.LANGFUSE_SECRET_KEY,
    #         session_id=session_id,
    #     )
    #     callbacks.append(langfuse_handler)
    return callbacks
