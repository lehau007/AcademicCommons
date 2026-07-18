from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
)
from app.db.session import get_session
from app.models import User
from app.schemas.auth import (
    LoginRequest,
    ResendVerificationRequest,
    ResendVerificationResponse,
    TokenResponse,
    UserCreate,
    UserRead,
    VerifyEmailResponse,
)
from app.services import email_verification
from app.services.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: SessionDep) -> TokenResponse:
    user = await authenticate_user(session, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user.is_email_verified:
        # Signal the frontend to show the "resend verification" UI. Do not leak
        # which emails are registered beyond what login already revealed.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="email_not_verified",
        )

    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
async def me(user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(user)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    session: SessionDep,
) -> UserRead:
    """Public student self-registration. The role is always forced to "student".

    A verification email is sent (via the configured email backend) holding a
    single-use Redis token. The user is created with ``is_email_verified=False``
    and cannot log in until they click the link → ``POST /auth/verify-email``.
    """
    existing = await session.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="student",
        full_name=payload.full_name,
        is_email_verified=False,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    await _dispatch_verification_email(user)
    return UserRead.model_validate(user)


@router.post("/verify-email", response_model=VerifyEmailResponse, status_code=status.HTTP_200_OK)
async def verify_email(
    token: str,
    session: SessionDep,
) -> VerifyEmailResponse:
    """Redeem a single-use verification token and mark the user as verified."""
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing verification token")

    user_id = await email_verification.consume_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token is invalid or has expired",
        )

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token is invalid or has expired",
        )

    if not user.is_email_verified:
        user.is_email_verified = True
        await session.commit()
        await session.refresh(user)

    return VerifyEmailResponse(user=UserRead.model_validate(user))


@router.post("/resend-verification", response_model=ResendVerificationResponse)
async def resend_verification(
    payload: ResendVerificationRequest,
    session: SessionDep,
) -> ResendVerificationResponse:
    """Re-send the verification email.

    Always returns ``ok=true`` so an attacker cannot enumerate which addresses
    are registered. Per-user cooldown is enforced server-side via Redis.
    """
    user = await session.scalar(select(User).where(User.email == payload.email))
    if user is not None and not user.is_email_verified:
        if await email_verification.set_resend_cooldown(user.id):
            await _dispatch_verification_email(user)

    return ResendVerificationResponse()


async def _dispatch_verification_email(user: User) -> None:
    settings = get_settings()
    token = await email_verification.create_token(user.id)
    verify_url = f"{settings.app_base_url.rstrip('/')}/verify-email?token={token}"
    html = (
        f"<p>Xin chào {user.full_name or 'bạn'},</p>"
        f"<p>Vui lòng xác minh địa chỉ email của bạn để hoàn tất đăng ký trên Academic Commons:</p>"
        f'<p><a href="{verify_url}">{verify_url}</a></p>'
        f"<p>Liên kết có hiệu lực {settings.email_verification_ttl_minutes} phút "
        f"và chỉ được sử dụng một lần.</p>"
        f"<p>Nếu bạn không đăng ký tài khoản, vui lòng bỏ qua email này.</p>"
    )
    await send_email(
        to=user.email,
        subject="Xác minh email — Academic Commons",
        html=html,
    )