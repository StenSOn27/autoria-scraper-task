from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from loguru import logger
from database.models.car import Car

class CarRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_car(self, data: dict) -> bool:
        try:
            car = Car(**data)
            self.session.add(car)
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            return False
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[REPO ERROR] Saving error {data.get('url')}: {e}")
            raise e
