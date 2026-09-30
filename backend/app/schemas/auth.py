#auth用スキーマ
from pydantic import BaseModel
from typing import Optional

#POST/auth用
class AuthRequest(BaseModel):
    id_token: str

class AuthResponse(BaseModel):
    registration_required: bool
    gu_api_jwt: Optional[str] = None
    registration_token: Optional[str] = None

#登録用
from datetime import date

class RegisterRequest(BaseModel):
    post_code: str
    birthday: date
    sex: str

#レスポンス用
class RegisteredUserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    post_code: str
    birthday: date
    sex: str

class RegisterResponse(BaseModel):
    gu_api_jwt: str
    user: RegisteredUserResponse


class UserInfoUserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    post_code: Optional[str]
    birthday: Optional[date]
    sex: Optional[str]


class UserInfoResponse(BaseModel):
    user: UserInfoUserResponse
    cart_count: int