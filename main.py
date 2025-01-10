from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
import models
from database import engine, Sessionlocal

app = FastAPI()

# Create tables in the database if they do not exist
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class ChoiceResponse(BaseModel):
    id: int
    choice_text: str
    question_id: int

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session,Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_questions(question_id:int, db:db_dependency):
    result=db.query(models.Questions).filter(models.Questions.id==question_id).first()
    if not result:
        raise HTTPException(status_code=404,detail='Question is not found')
    return result


@app.get("/choices/{question_id}", response_model=List[ChoiceResponse])
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choice).filter(models.Choice.question_id == question_id).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")

    return result

    
@app.post("/questions/")
async def create_questions(question: QuestionBase, db:db_dependency):
    try:
        # Create a new question
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # Add choices for the question
        for choice in question.choices:
            db_choice = models.Choice(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,  # Ensure that you have this attribute
                question_id=db_question.id
            )
            db.add(db_choice)
        
        # Commit the changes after adding all choices
        db.commit()

        return {"message": "Question and choices created successfully", "question_id": db_question.id}
    
    except Exception as e:
        # Log the error for debugging and return a 500 Internal Server Error with the exception message
        print(f"Error: {str(e)}")  # You can log this to a file if needed
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/check_answer/")
async def check_answer(question_id: int, choice_id: int, db: db_dependency):
    # Query the choice to check if it's correct
    choice = db.query(models.Choice).filter(models.Choice.id == choice_id, models.Choice.question_id == question_id).first()
    
    if not choice:
        raise HTTPException(status_code=404, detail="Choice not found for the question")

    # Check if the answer is correct
    if choice.is_correct:
        return {"message": "Correct answer!"}
    else:
        return {"message": "Incorrect answer!"}