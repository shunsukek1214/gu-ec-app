

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_registration_token,
)
from app.db.database import get_db
from app.models import User
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.google_auth_service import verify_google_id_token
from sqlalchemy.exc import IntegrityError

from app.api.deps import (
    get_current_user_id,
    get_registration_payload,
)
from app.schemas.auth import (
    AuthRequest,
    AuthResponse,
    RegisterRequest,
    RegisterResponse,
    RegisteredUserResponse,
    UserInfoResponse,
    UserInfoUserResponse,
)
from app.models import User, CartItem

#POST/auth
#Google ID Token受信
# ↓
# Googleで検証
# ↓
# google_sub取得
# ↓
# users検索
# ↓
# 登録済み？

router = APIRouter(
    tags=["auth"],
)

@router.post(
    "/auth",
    response_model=AuthResponse,
)

def authenticate(
    auth_request: AuthRequest,
    db: Session = Depends(get_db),
):
    #googleIDtokenを検証
    try:
        google_user = verify_google_id_token(
            auth_request.id_token
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token"
        )
    
    #user tableを検索
    user = (
        db.query(User)
        .filter(
            User.google_sub == google_user["google_sub"]
        )
        .first()
    )

    #登録済みユーザーの場合
    if user:
        gu_api_jwt = create_access_token(
            user_id=user.user_id             
        )
        return AuthResponse(
            registration_required=False,
            gu_api_jwt=gu_api_jwt,
        )
    
    #未登録ユーザーの場合の処理
    registration_token = create_registration_token(
        google_sub=google_user["google_sub"],
        email=google_user["email"],
        name=google_user["name"],
    )
    return AuthResponse(
        registration_required=True,
        registration_token=registration_token,
    )

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    register_request: RegisterRequest,
    registration_data: dict = Depends(
        get_registration_payload
    ),
    db: Session = Depends(get_db),
):
    #重複ユーザーの確認
    existing_user = (
        db.query(User)
        .filter(
            User.google_sub == registration_data["sub"]
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    
    user = User(
        google_sub=registration_data["sub"],
        name=registration_data["name"],
        email=registration_data["email"],
        post_code=register_request.post_code,
        birthday=register_request.birthday,
        sex=register_request.sex,
    )

    #DBへインサート
    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    
    #GU API JWT発行
    gu_api_jwt = create_access_token(
        user_id=user.user_id
    )

    return RegisterResponse(
        gu_api_jwt=gu_api_jwt,
        user=RegisteredUserResponse(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            post_code=user.post_code,
            birthday=user.birthday,
            sex=user.sex,
        ),
    )

#ユーザー情報(カート情報含む)
@router.get(
    "/user_info",
    response_model=UserInfoResponse,
)
def get_user_info(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    #ユーザー情報取得
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    #カート件数
    cart_count = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .count()
    )
    return UserInfoResponse(
        user=UserInfoUserResponse(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            post_code=user.post_code,
            birthday=user.birthday,
            sex=user.sex,
        ),
        cart_count=cart_count,
    )