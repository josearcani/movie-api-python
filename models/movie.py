from sqlalchemy import Column, Float, Integer, String
from config.database import Base # import from config

class Movie(Base):
    
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(String)
    rating = Column(Float)
    category = Column(String)



