from typing import Annotated

from fastapi import APIRouter, status, Response, Header, Depends
from sqlalchemy.orm import Session

from services import session_service
from config.logger import logger
from config.database import get_db
from schemas.session_schema import UserSigninParams, UserSigninResponse

session_router = APIRouter(tags=["session"])


@session_router.post("/signup")
async def signup_user() -> None:
    try:
        pass
    except Exception as e:
        logger.exception(e)
        raise e


@session_router.post(
    "/signin", response_model=UserSigninResponse, status_code=status.HTTP_200_OK
)
async def signin_user(
    params: UserSigninParams,
    response: Response,
    ip_address: Annotated[str, Header(alias="x-forwarded-for")],
    db: Session = Depends(get_db),
) -> UserSigninResponse:
    try:
        params.ip_address = ip_address
        user, access_token = session_service.signin_user(db, params)
        response.headers["Authorization"] = f"Bearer {access_token}"
        return UserSigninResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile_no=user.mobile_no,
            role=user.role.name,
        )
    except Exception as e:
        logger.exception(e)
        raise e
