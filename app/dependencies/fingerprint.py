from fastapi import Request

from config.constants import GENERAL_CONFIGS
from config.redis_client import redis_client
from exceptions.custom_errors import ForbiddenException, BadRequestException


async def verify_session_fingerprint(request: Request) -> None:
    session_id = request.headers.get("X-Session-ID")
    user_agent = request.headers.get("user-agent")
    cookie_token = request.cookies.get(GENERAL_CONFIGS.SESSION_COOKIE_NAME)

    if not session_id or not user_agent or not cookie_token:
        raise BadRequestException("Missing session headers or cookie")

    redis_key_cookie = f"session:{session_id}:cookie"
    redis_key_ua = f"session:{session_id}:user_agent"

    stored_cookie = await redis_client.get(redis_key_cookie)
    stored_ua = await redis_client.get(redis_key_ua)

    # first time: store
    if stored_cookie is None:
        await redis_client.set(redis_key_cookie, cookie_token, ex=86400)
        await redis_client.set(redis_key_ua, user_agent, ex=86400)
    elif stored_cookie.decode() != cookie_token or stored_ua.decode() != user_agent:
        raise ForbiddenException("Session/User-Agent mismatch")
