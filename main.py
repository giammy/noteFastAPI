from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import null
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import Note
import models
import schemas

# Create the database: we explicity import Note from models.py
# so the table "note" is created in the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/note", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, session: Session = Depends(get_session)):

    # create an instance of the Note model
    dbEntry = models.Note(rid = note.rid, lid = note.lid, type = note.type, data = note.data)

    # add it to the session and commit it
    session.add(dbEntry)
    session.commit()
    # refresh is needed to get the id
    session.refresh(dbEntry)

    # return the note object
    return dbEntry

@app.put("/note/{id}", response_model=schemas.Note)
def update_todo(id: int, data: str, session: Session = Depends(get_session)):

    # get the note with the given id
    note = session.query(models.Note).get(id)

    # update note with the given task (if an item with the given id was found)
    if note:
        note.data = data
        session.commit()

    # check if note with given id exists. If not, raise exception and return 404 not found response
    if not note:
        raise HTTPException(status_code=404, detail=f"note with id {id} not found")

    return note

@app.delete("/note/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, session: Session = Depends(get_session)):

    # get the note item with the given id
    note = session.query(models.Note).get(id)

    # if note with given id exists, delete it from the database. Otherwise raise 404 error
    if note:
        session.delete(note)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"note with id {id} not found")

    return None

@app.get("/")
def root():
    return "note"

@app.get("/note/", response_model=List[schemas.Note])
def search_note_on_field(id: int | None = None, rid: int | None = None, lid: int | None = None, type: str | None = None, data: str | None = None, session: Session = Depends(get_session)):
    # usage example: http://127.0.0.1:8000/note/?rid=0&lid=10&type=TTT&data=ddd

    # create a dictionary with nonull values
    search_dict = {k: v for k, v in {'id': id, 'rid': rid, 'lid': lid, 'type': type, 'data': data}.items() if v is not None}
    note = session.query(models.Note).filter_by(**search_dict).all()

    # check if notes with given criteria exist. If not, raise exception and return 404 not found response
    if not note:
        raise HTTPException(status_code=404, detail=f"note not found")

    return note

@app.get("/note", response_model = List[schemas.Note])
def read_note_list(session: Session = Depends(get_session)):
    
    # get all notes
    note_list = session.query(models.Note).all()

    return note_list
