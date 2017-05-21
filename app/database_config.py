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

class User(Base):
	__tablename__="user"

	id = Column(Integer, primary_key=True)
	name = Column(String(500), nullable=False, unique=True)
	user_answer_id = Column(Integer, ForeignKey('user_answers.id'))
	user_question_id = Column(Integer, ForeignKey('user_questions.id'))
	score = Column(Integer)

	def __init__(self, name, user_answer_id, user_question_id):
		self.name = name
		self.user_answer_id = user_answer_id
		self.user_question_id = user_question_id

class UserAnswers(Base):
	__tablename__ = 'user_answers'
	id = Column(Integer,primary_key=True)
	first = Column(Integer)
	second = Column(Integer)
	third = Column(Integer)
	fourth = Column(Integer)
	fifth = Column(Integer)
	sixth = Column(Integer)
	seventh = Column(Integer)
	eight = Column(Integer)
	ninth = Column(Integer)
	tenth = Column(Integer)

class UserQuestions(Base):
	__tablename__ = 'user_questions'
	id = Column(Integer,primary_key=True)
	first = Column(Integer)
	second = Column(Integer)
	third = Column(Integer)
	fourth = Column(Integer)
	fifth = Column(Integer)
	sixth = Column(Integer)
	seventh = Column(Integer)
	eight = Column(Integer)
	ninth = Column(Integer)
	tenth = Column(Integer)

engine = create_engine('sqlite:///quizzzz.db')


Base.metadata.create_all(engine)
