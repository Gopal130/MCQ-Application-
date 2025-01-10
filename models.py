from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

# Use the correct PascalCase name
class Questions(Base):  
    __tablename__ = 'questions'  # Define table name correctly

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

    # Define relationship with choices
    choices = relationship("Choice", back_populates="question")


class Choice(Base):  
    __tablename__ = 'choices'  # Define table name correctly

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

    # Define back relationship with Question
    question = relationship("Questions", back_populates="choices")
