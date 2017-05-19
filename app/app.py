from flask import Flask, render_template, redirect, url_for
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_config import Base, Quiz, Question, Answer
import random
from random import shuffle
app = Flask(__name__)


ENGINE = create_engine('sqlite:///quiz.db')
Base.metadata.bind = ENGINE

DBSession = sessionmaker(bind=ENGINE)
session = DBSession()


@app.route('/')
def HomePage():
    quizzes = session.query(Quiz).all()
    for u in quizzes:
        print u.__dict__
    return render_template('index.html', quizzes=quizzes)

@app.route('/python')
@app.route('/python/')
def RedirectToFirst():
    return redirect(url_for('PythonQuiz', question_id = 1))

@app.route('/python/<int:question_id>')
def PythonQuiz(question_id):
    question = session.query(Question).get(question_id)
    correct_answer = session.query(Answer).get(question_id)
    query = session.query(Answer)
    row_count = int(query.count())
    python_answers_count = session.query(Question).filter(Question.quiz_id == 1).count()
    
    if question_id > python_answers_count:
        return redirect(url_for('EndResult'))
    first_random_row = query.offset(int(row_count * random.random())).first()
    second_random_row = query.offset(int(row_count * random.random())).first()

    all_answers = [first_random_row, second_random_row, correct_answer]
    shuffle(all_answers)
    return render_template('quizsheet.html', question=question, answers=all_answers,
                 questions_row_count=python_answers_count, quiz_name = "python")

@app.route('/python/end')
def EndResult():
    return 'end'



@app.route('/java')
def JavaQuiz():
    return 'java'


@app.route('/cplusplus')
def CplusplusQuiz():
    cplusplus_id = 2
    questions = session.query(Question).filter(Question.id == cplusplus_id)
    answers = session.query(Answer).filter(Answer.question_id > 19).all()
    complect = dict(zip(questions, answers))
    #render_template('questions.html', complect=complect)
    return render_template('questions.html', complect=complect)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
