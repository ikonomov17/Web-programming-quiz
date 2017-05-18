from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_config import Base, Quiz, Question, Answer
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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
