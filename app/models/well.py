from sqlalchemy.orm import relationship

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date

class Well(Base):
    __tablename__ = 'wells'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    depth = Column(Float)
    status_id = Column(Integer, ForeignKey('well_statuses.id'))
    drilling_date = Column(Date)
    license_id = Column(Integer, ForeignKey('licenses.id'))
    field_id = Column(Integer, ForeignKey('fields.id'))

    license = relationship("License", back_populates="wells")
    field = relationship("Field", back_populates="wells")
    status = relationship("WellStatus")