from sqlalchemy import Column, Integer, String
from database import Base

# Define the note class inheriting from Base
class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    rid = Column(Integer)
    lid = Column(Integer)
    type = Column(String(64))
    data = Column(String(1024))






