from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from src.auth.utils import decode_access_token
from fastapi.security.http import HTTPAuthorizationCredentials

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error = auto_error)

    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.token_is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid or expired token'
            )
        

        self.verify_token_data(token_data)

        return token_data

    def token_is_valid(self, token: str) -> bool:
        decoded_token = decode_access_token(token)
        return True if decoded_token is not None else False
    

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError('Please implement this method in child classes')

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Please provide an access token'
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if not token_data or not token_data['refresh']:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Please provide a valid refresh token'
            )

