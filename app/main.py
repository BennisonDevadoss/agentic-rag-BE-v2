# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/

import uvicorn
from fastapi import FastAPI

from config.logger import logger
from config.settings import SETTINGS
from config.constants import ENVIRONMENT_TYPE
from routers.v1.router import v1_router
from config.cors_options import configure_cors
from exceptions.http_exception_filter import register_exception_handlers


# Create and configure the FastAPI application
def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentic RAG Server",
        description="Backend server for Agentic RAG",
        version="0.0.1",
        docs_url=(
            None if SETTINGS.ENVIRONMENT == ENVIRONMENT_TYPE.PRODUCTION else "/docs"
        ),
        redoc_url=(
            None if SETTINGS.ENVIRONMENT == ENVIRONMENT_TYPE.PRODUCTION else "/redoc"
        ),
    )

    # Apply CORS settings and register exception handlers
    configure_cors(app)
    register_exception_handlers(app)

    # Include routers
    app.include_router(v1_router)

    return app


# Initialize the app
app = create_app()


# Define the root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from Agentic RAG System!!!"}


# Run the application with uvicorn
if __name__ == "__main__":
    # https://fsymbols.com/
    print(  # noqa: T201
        """
░█████╗░░██████╗░███████╗███╗░░██╗████████╗██╗░█████╗░  ██████╗░░█████╗░░██████╗░
██╔══██╗██╔════╝░██╔════╝████╗░██║╚══██╔══╝██║██╔══██╗  ██╔══██╗██╔══██╗██╔════╝░
███████║██║░░██╗░█████╗░░██╔██╗██║░░░██║░░░██║██║░░╚═╝  ██████╔╝███████║██║░░██╗░
██╔══██║██║░░╚██╗██╔══╝░░██║╚████║░░░██║░░░██║██║░░██╗  ██╔══██╗██╔══██║██║░░╚██╗
██║░░██║╚██████╔╝███████╗██║░╚███║░░░██║░░░██║╚█████╔╝  ██║░░██║██║░░██║╚██████╔╝
╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░╚════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░

building the best AI Application.
https://github.com/BennisonDevadoss/AgenticRAG
"""  # noqa: E501
    )
    logger.info(f"Server listening at http://{SETTINGS.HOST}:{SETTINGS.PORT}")
    uvicorn.run(
        "main:app",
        host=SETTINGS.HOST,
        port=SETTINGS.PORT,
        reload=SETTINGS.ENVIRONMENT != ENVIRONMENT_TYPE.PRODUCTION,
        workers=1,
        # logger="info",
    )
