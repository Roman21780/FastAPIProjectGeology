from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    owner_id = Column(Integer, ForeignKey('companies.id'))

    fields = relationship("Field", back_populates="license")
    wells = relationship("Well", back_populates="license")
    owner = relationship("Company", back_populates="licenses")