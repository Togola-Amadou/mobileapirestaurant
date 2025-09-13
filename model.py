from sqlalchemy import Column, Integer, String
from database import Base   


class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)