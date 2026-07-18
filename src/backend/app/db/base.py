from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import model modules so Alembic autogenerate can see Base.metadata.
from app import models as models  # noqa: E402,F401
