from core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .mixins import TimestampMixin


class UserModel(TimestampMixin, Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(255), nullable=False)

    password: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
