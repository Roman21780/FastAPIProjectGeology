from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    licenses = relationship("License", back_populates="owner")


class WellStatus(Base):
    __tablename__ = 'well_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))