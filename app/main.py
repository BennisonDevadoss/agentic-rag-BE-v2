# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/

from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.logger import logger
from config.settings import SETTINGS
from config.constants import ENVIRONMENT_TYPE
from routers.v1.router import v1_router
from config.cors_options import configure_cors
from vector_db.milvus_db import MilvusService
from agents.common.checkpointer import checkpointer
from exceptions.http_exception_filter import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any]:
    checkpointer.setup()
    MilvusService.create_and_reset_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        debug=SETTINGS.DEBUG,
        title="Agentic RAG Server",
        description="Backend server for Agentic RAG",
        version="0.0.1",
        lifespan=lifespan,
        docs_url=(
            None
            if SETTINGS.ENVIRONMENT == ENVIRONMENT_TYPE.PRODUCTION.value
            else "/docs"
        ),
        redoc_url=(
            None
            if SETTINGS.ENVIRONMENT == ENVIRONMENT_TYPE.PRODUCTION.value
            else "/redoc"
        ),
    )

    configure_cors(app)
    register_exception_handlers(app)

    app.include_router(v1_router)

    return app


app = create_app()


@app.get("/")
async def root() -> dict[str, str | bool]:
    return {
        "env": SETTINGS.ENVIRONMENT,
        "debug": SETTINGS.DEBUG,
        "message": "Hello from Agentic RAG System!!!",
    }


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
    logger.info(
        f"🚀 Server listening at http://{SETTINGS.HOST}:{SETTINGS.PORT} in {SETTINGS.ENVIRONMENT.upper()} environment 🌍"  # noqa: E501
    )
    uvicorn.run(
        "main:app",
        host=SETTINGS.HOST,
        port=SETTINGS.PORT,
        reload=SETTINGS.ENVIRONMENT != ENVIRONMENT_TYPE.PRODUCTION,
        workers=1,
    )
