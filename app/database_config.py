import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Quiz(Base):
	__tablename__ = 'quizzes'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	programming_language = Column(String(50), nullable=False)
	message = Column(String(250), nullable = False)

class Question(Base):
	__tablename__ = 'questions'

	id = Column(Integer, primary_key=True)
	text = Column(String(500), nullable=False)
	quiz_id = Column(Integer, ForeignKey('quizzes.id'))
	quiz = relationship(Quiz)

class Answer(Base):
	__tablename__ = 'answers'

	id = Column(Integer, primary_key=True)
	text = Column(String(500), nullable=False)
	question_id = Column(Integer, ForeignKey('questions.id'))
	isCorrect = Column(Integer,ForeignKey('quizzes.id'))
	quiz = relationship(Question)

engine = create_engine('sqlite:///quizz.db')


Base.metadata.create_all(engine)
