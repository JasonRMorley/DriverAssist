from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    driver_number: Mapped[int] = mapped_column(primary_key=True)
    line_number: Mapped[int] = mapped_column(primary_key=True)

