from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class UserCreate(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    role: str = Field(pattern="^(student|reviewer|admin)$")
    full_name: str | None = None


class UserUpdate(BaseModel):
    role: str | None = Field(default=None, pattern="^(student|reviewer|admin)$")
    is_active: bool | None = None


class UserRead(BaseModel):
    id: UUID
    email: str
    role: str
    full_name: str | None = None
    is_active: bool = True
    is_email_verified: bool = False

    model_config = {"from_attributes": True}

    @field_validator("is_active", mode="before")
    @classmethod
    def _default_unset_is_active_to_true(cls, value: bool | None) -> bool:
        # The `users.is_active` column only gets its true default at INSERT
        # time (server_default); a User constructed in Python but never
        # persisted/refreshed reads back as None here. Treat that the same
        # as the DB default (active) rather than failing validation.
        return True if value is None else value

    @field_validator("is_email_verified", mode="before")
    @classmethod
    def _default_unset_email_verified_to_false(cls, value: bool | None) -> bool:
        # Same reasoning as is_active: server_default only fills at INSERT time.
        return False if value is None else value


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


class VerifyEmailResponse(BaseModel):
    verified: bool = True
    user: UserRead


class ResendVerificationRequest(BaseModel):
    email: str = Field(min_length=3)


class ResendVerificationResponse(BaseModel):
    # Always returns ok=true regardless of whether the email exists, so the
    # endpoint cannot be used to enumerate which addresses are registered.
    ok: bool = True
