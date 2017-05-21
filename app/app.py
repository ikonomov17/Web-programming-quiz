from flask import Flask, render_template, redirect, url_for
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_config import Base, Quiz, Question, Answer
import random
from random import shuffle
app = Flask(__name__)


ENGINE = create_engine('sqlite:///quizz.db')
Base.metadata.bind = ENGINE

DBSession = sessionmaker(bind=ENGINE)
session = DBSession()
first_questions = dict();

@app.route('/')
def HomePage():
    quizzes = session.query(Quiz).order_by(Quiz.id).all()

    data = dict()

    for quiz in quizzes:
        first_question_id = session.query(Question).filter(Question.quiz_id == quiz.id).first().id
        first_questions.update({quiz.programming_language: first_question_id})
        data.update({quiz :first_question_id})

    return render_template('index.html', data=data)

@app.route('/<string:lang>')
@app.route('/<lang>/')
def RedirectToFirst(lang):
    return redirect(url_for('QuizResponse', lang = lang, question_id = first_questions[lang]))

# @app.route('/python/<int:question_id>')
# def PythonQuiz(question_id):
#     question = session.query(Question).get(question_id)
#     correct_answer = session.query(Answer).get(question_id)
#     query = session.query(Answer)
#     python_answers_count = session.query(Question).filter(Question.quiz_id == 1).count()
    
#     if question_id > python_answers_count:
#         return redirect(url_for('EndResult'))

#     first_random_row = query.offset(int(python_answers_count * random.random())).first()
#     second_random_row = query.offset(int(python_answers_count * random.random())).first()

#     all_answers = [first_random_row, second_random_row, correct_answer]
#     shuffle(all_answers)
#     return render_template('quizsheet.html', question=question, answers=all_answers,
#                  questions_row_count=python_answers_count, quiz_name = "python")

@app.route('/python/end')
def EndResult():
    return 'end'



@app.route('/<string:lang>/<int:question_id>')
def QuizResponse(lang, question_id):
    current_language = session.query(Quiz).filter(Quiz.programming_language == lang).first()
    # check if there is such language in database, if not should return error page
    if current_language is None:
        return render_template('questions.html',programming_language='no such language')

    current_language_id = current_language.id
    questions = session.query(Question).filter(Question.quiz_id == current_language_id).all()
    # get all questions id's because question for one language may not be one after another
    all_questions_ids = []
    for q in questions:
        all_questions_ids.append(q.id)

    #return render_template('questions.html',programming_language=21 in all_questions_ids)
    # check if the question_id passed in url is valid for there lang
    question_id = int(question_id)
    if question_id not in all_questions_ids:
      return render_template('proba.html',programming_language='no such question for this lang')

    answers = session.query(Answer).filter(Answer.question_id.in_(all_questions_ids))
    exact_question = session.query(Question).get(question_id)
    correct_answer = session.query(Answer).get(question_id).text
    
    lang_answers_count = len(all_questions_ids)
    first_random_row = answers.offset(int(lang_answers_count * random.random())).first().text
    second_random_row = answers.offset(int(lang_answers_count * random.random())).first().text
    all_answers = [first_random_row, second_random_row, correct_answer]
    shuffle(all_answers)
    return render_template('quizsheet.html',question_ids=all_questions_ids,question=exact_question,
            answers = all_answers,quiz_name = lang)


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
