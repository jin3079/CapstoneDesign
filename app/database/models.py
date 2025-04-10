from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    places = relationship('Place', back_populates='category')

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    status = Column(String)
    built_year = Column(Integer)
    built_month = Column(Integer)
    built_date = Column(Date)
    capacity = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='places')