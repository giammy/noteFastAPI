from pydantic import BaseModel

# Create Schema (Pydantic Model)
class NoteCreate(BaseModel):
    rid: int
    lid: int
    type: str
    data: str

# Complete ToDo Schema (Pydantic Model)
class Note(BaseModel):
    id: int
    rid: int
    lid: int
    type: str
    data: str
    
    class Config:
        orm_mode = True
