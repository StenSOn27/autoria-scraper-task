from sqlalchemy import (
    Integer, DateTime, String, func, BigInteger
)
from datetime import datetime
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    price_usd: Mapped[int] = mapped_column(Integer)
    odometer: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[int] = mapped_column(BigInteger)
    image_url: Mapped[str] = mapped_column(String(2048))
    images_count: Mapped[int] = mapped_column(Integer)
    car_number: Mapped[str] = mapped_column(String(255))
    car_vin: Mapped[str] = mapped_column(String(255))
    
    datetime_found: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now()
    )
