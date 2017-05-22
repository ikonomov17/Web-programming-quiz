from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker,scoped_session
from database_config import Base, Quiz, Question, Answer, User, UserAnswers, UserQuestions
import random
from random import shuffle
app = Flask(__name__)


ENGINE = create_engine('sqlite:///quizzzz.db')
Base.metadata.bind = ENGINE

DBSession = sessionmaker(bind=ENGINE)
session = DBSession()

def GetLanguagesWithFirstQuestionId():
    first_questions = dict()
    quizzes = session.query(Quiz).order_by(Quiz.id).all()

    for quiz in quizzes:
        first_question_id = session.query(Question).filter(Question.quiz_id == quiz.id).first().id
        first_questions.update({quiz: first_question_id})

    return first_questions

def IsLanguageInDatabase(lang, db):
    for record in db:
        if(record.programming_language == lang):
            return True
    return False

@app.route('/')
def HomePage():
    data = GetLanguagesWithFirstQuestionId()

    return render_template('index.html', data=data)

@app.route('/<string:lang>/add_user', methods=['GET','POST'])
def AddUser(lang):
    if request.method == 'GET':
        return render_template('proba.html')
    else:
        user_answers = UserAnswers()
        user_questions = UserQuestions()
        session.add(user_answers)
        session.add(user_questions)
        session.commit()
        user_questions_id = session.query(UserQuestions).order_by(desc(UserQuestions.id)).first().id
        user_answers_id = session.query(UserAnswers).order_by(desc(UserAnswers.id)).first().id
        current_user = User(request.form['name'], user_answers_id, user_questions_id)
        session.add(current_user)
        session.commit()
        first_questions = GetLanguagesWithFirstQuestionId()
        return redirect(url_for('QuizResponse', lang = lang, question_id = first_questions[lang]))

@app.route('/<string:lang>')
@app.route('/<string:lang>/')
def RedirectToAddUser(lang):
    first_questions = GetLanguagesWithFirstQuestionId()
    LangIsInDict = IsLanguageInDatabase(lang, first_questions) 
    if LangIsInDict:
        return redirect(url_for('AddUser', lang = lang))
    else:
        return render_template('error404.html',message='No such language :))')

@app.route('/<string:lang>/<int:question_id>')
def QuizResponse(lang, question_id):
    current_language = session.query(Quiz).filter(Quiz.programming_language == lang).first()
    # check if there is such language in database, if not should return error page
    if current_language is None:
        return render_template('error404.html',message='No such language :))')

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
      return render_template('error404.html',message='No question with that id for this quiz')

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



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
