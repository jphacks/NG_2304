from typing import Optional
from api.settings import settings
from api.db.dao.user_dao import UserDAO
from fastapi import Cookie, Depends, HTTPException, Header, status
from typing import TYPE_CHECKING
from jose import ExpiredSignatureError, JWTError, jwt

if TYPE_CHECKING:
    from api.web.api.users.shema import SessionUser


async def is_authenticated(
    user_dao: UserDAO = Depends(),
    access_token: str = Cookie(default=None),
    session_id: str = Cookie(default=None),
    authorization: Optional[str] = Header(default=None),
) -> "UserModelDTO":
    from api.web.api.users.shema import SessionUser

    if authorization is None and access_token is None:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization credentials is missing.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_request"'},
        )

    if authorization is not None:
        jwt_token = authorization.rsplit(maxsplit=1)[-1]
    elif access_token is not None:
        jwt_token = access_token
    else:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    try:
        payload = jwt.decode(
            jwt_token, settings.token_secret_key, algorithms=[settings.token_algorithm]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    user = await user_dao.get_user(payload["user_id"])

    if user is not None:
        # access_token gets
        # print(user.github_tokens)
        # if access_token invalid:
        #    if refresh_token is valid:
        #      reload_refresh_token
        #    else:
        #       return 401
        authenticated_user = SessionUser.model_validate(user, from_attributes=True)
        if session_id is not None:
            authenticated_user.session_cert = session_id
        return authenticated_user

    raise HTTPException(
        status_code=404,
        detail="Not found user.",
        headers={"WWW-Authenticate": 'Bearer error="not_found_user"'},
    )
