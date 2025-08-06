from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Field(Base):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    license_id = Column(Integer, ForeignKey('licenses.id'))
    coordinates = Column(String)  # Можно использовать PostGIS geometry при необходимости

    license = relationship("License", back_populates="fields")
    wells = relationship("Well", back_populates="field")