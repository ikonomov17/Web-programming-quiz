from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_config import Base, Quiz, Question, Answer
import random
from random import shuffle
app = Flask(__name__)


engine = create_engine('sqlite:///quiz.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def HomePage():
	quizzes = session.query(Quiz).all();
	for u in quizzes:
		print u.__dict__
	return render_template('index.html', quizzes = quizzes)

@app.route('/python')
def PythonQuiz():
	question = session.query(Question).first()
	correctAnswer = session.query(Answer).get(question.id)
	query = session.query(Answer)
	rowCount = int(query.count())
	firstRandomRow = query.offset(int(rowCount*random.random())).first()
	secondRandomRow = query.offset(int(rowCount*random.random())).first()

	allAnswers = [firstRandomRow,secondRandomRow,correctAnswer]
	shuffle(allAnswers)
	return render_template('quizsheet.html', question = question, answers = allAnswers)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
