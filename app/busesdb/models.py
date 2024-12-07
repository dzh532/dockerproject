from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Bus(Base):
    __tablename__ = "busestest"

    gos_number = Column(String(10), primary_key=True)
    capacity = Column(Integer, nullable=False)
    is_air_conditioner = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Bus(gos_number={self.gos_number}, capasity={self.capacity}, is_air_cond={self.is_air_conditioner})>"