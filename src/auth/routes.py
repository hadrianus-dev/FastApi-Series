from datetime import timedelta, datetime
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.api.v1.dependencies import RefreshTokenBearer
from .schemes import UserCreateSchema, UserLoginSchema, UserSchema
from .services import UserService
from src.database.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_access_token, verify_password

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", response_model = UserSchema, status_code = status.HTTP_201_CREATED)
async def signup(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(session, email)

    if user_exists:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'User with email already exists')
     
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post("/login", status_code = status.HTTP_200_OK)
async def login(login_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(session, login_data.email, as_dict = False)

    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Invalid credentials')
    if user is not None:
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Invalid credentials')
        access_token = create_access_token(user_data={
            'email': user.email,
            'uid': str(user.uid)
        })

        refresh_token = create_access_token(
            user_data={
                'email': user.email,
                'uid': str(user.uid)
            },
            refresh = True,
            expiry = timedelta(days = 2)
        )

        return JSONResponse(
            content = {
                'message': 'Login Successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'uid': str(user.uid),
                    'email': user.email
                }
            },
            status_code = status.HTTP_200_OK
        )
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Invalid credentials: Ivalid Email or Password')


@auth_router.get("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    """
    Refreshes an access token for a user who has a valid refresh token.
    """
    if token_data["exp"] < datetime.now().timestamp():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    access_token = create_access_token(user_data=token_data["user"])

    return JSONResponse(
        content={"message": "Token refreshed successfully", "access_token": access_token},
        status_code=status.HTTP_200_OK,
    )
