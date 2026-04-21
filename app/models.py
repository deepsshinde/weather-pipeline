from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)