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

one_to_ten = ['first','second','third','fourth','fifth','sixth','sevent','eight','ninth','tenth']

# Helper methods
def GetLanguagesWithFirstQuestionId():
    first_questions = dict()
    quizzes = session.query(Quiz).order_by(Quiz.id).all()

    for quiz in quizzes:
        first_question_id = session.query(Question).filter(Question.quiz_id == quiz.id).first().id
        first_questions.update({quiz: first_question_id})

    return first_questions

def GetOnlyQuizNamesAndFirstQuestionIds():
    quiz_names_and_ids = dict() 
    quizzes = GetLanguagesWithFirstQuestionId()

    # encode from unicode string to normal string with the encode function
    for quiz, id in quizzes.iteritems():
        quiz_names_and_ids.update({quiz.programming_language.encode('ascii','ignore'): id})

    return quiz_names_and_ids

def IsLanguageInDatabase(lang, db):
    for record in db:
        if(record.programming_language == lang):
            return True
    return False

def GetRandomRelatedAnswers(question_id):
    number = int(random.random() * 10)

    if number % 2 == 0:
        answers = session.query(Answer).filter(Answer.question_id == question_id).filter(Answer.isCorrect != 1).order_by(Answer.id).all()[:2]
        return answers
    else:
        answers = session.query(Answer).filter(Answer.question_id == question_id).filter(Answer.isCorrect != 1).order_by(desc(Answer.id)).all()[:2]
        return answers

def GetRandomQuestions(current_language_id):
    number = int(random.random() * 10)

    if number % 2 == 0:
        questions = session.query(Question).filter(Question.quiz_id == current_language_id).all()
        shuffle(questions)
        session.close()
        return questions[:10]
    else:
        questions = session.query(Question).filter(Question.quiz_id == current_language_id).order_by(desc(Question.id)).all()
        shuffle(questions)
        session.close()
        return questions[:10]

questions_for_user = 0

# Main program logic
@app.route('/')
def HomePage():
    data = GetLanguagesWithFirstQuestionId()

    return render_template('index.html', data=data)

@app.route('/<string:lang>/add_user', methods=['GET','POST'])
def AddUser(lang):
    if request.method == 'GET':
        return render_template('quizname.html')
    else:
        user_answers = UserAnswers()
        user_questions = UserQuestions()
        session.add(user_answers)
        session.add(user_questions)
        session.commit()
        user_questions_id = session.query(UserQuestions).order_by(desc(UserQuestions.id)).first().id
        user_answers_id = session.query(UserAnswers).order_by(desc(UserAnswers.id)).first().id
        current_user = User(request.form['username'], user_answers_id, user_questions_id)
        session.add(current_user)
        session.commit()
        session.rollback()
        first_questions = GetOnlyQuizNamesAndFirstQuestionIds()
        global questions_for_user
        lang_id = session.query(Quiz).filter(Quiz.programming_language == lang).first().id
        questions_for_user = GetRandomQuestions(lang_id)
        first_question_id = questions_for_user[0].id

        return redirect(url_for('QuizResponse', lang=lang, question_id=first_question_id))

@app.route('/<string:lang>')
@app.route('/<string:lang>/')
def RedirectToAddUser(lang):
    first_questions = GetLanguagesWithFirstQuestionId()
    LangIsInDict = IsLanguageInDatabase(lang, first_questions)
    if LangIsInDict:
        return redirect(url_for('AddUser', lang=lang))
    else:
        return render_template('error404.html', message='We have no quiz for this language :))')

@app.route('/<string:lang>/<int:question_id>', methods=['GET', 'POST'])
def QuizResponse(lang, question_id):
    all_questions_ids = []
    global questions_for_user
    questions = questions_for_user
    # get all questions id's because question for one language may not be one after another
        
    for q in questions:
        all_questions_ids.append(q.id)

    if request.method == 'GET':
        current_language = session.query(Quiz).filter(Quiz.programming_language == lang).first()
        # check if there is such language in database, if not should return error page
        if current_language is None:
            return render_template('error404.html', message='We have no quiz for this language :))')

        current_language_id = current_language.id
        

        #return render_template('questions.html',programming_language=21 in all_questions_ids)
        # check if the question_id passed in url is valid for there lang
        question_id = int(question_id)
        if question_id not in all_questions_ids:
            return render_template('error404.html', message='No question with that id for this quiz')
        lang_answers_count = len(all_questions_ids)
        answers = GetRandomRelatedAnswers(question_id)
        nonsense_answer = session.query(Answer).offset(int(lang_answers_count * random.random())).first().text
        correct_answer = session.query(Answer).filter(Answer.question_id == question_id).filter(Answer.isCorrect == 1).first().text
        answers_array = [answers[0].text, answers[1].text, correct_answer, nonsense_answer]
        shuffle(answers_array)
        exact_question = session.query(Question).get(question_id)
        
        return render_template('quizsheet.html', question_ids=all_questions_ids, question=exact_question,
                answers = answers_array, quiz_name = lang)
    else:
        last_user = session.query(User).order_by(desc(User.id)).first()
        last_user_answers = session.query(UserAnswers).filter(UserAnswers.id == last_user.user_answer_id).first()
        last_user_questions = session.query(UserQuestions).filter(UserQuestions.id == last_user.user_answer_id).first()
        # split the url get the last which should be the id and remove the "?" at the end
        current_question_id = request.full_path.encode('ascii','ignore').split("/")[2][:-1]
        current_answer_id = session.query(Answer).filter(Answer.text == request.form['answers']).first()
        current_question = int(request.form['current_q'].encode('ascii', 'ignore'))
        current_answer = request.form['answers']
        column_name = one_to_ten[current_question - 1]
        setattr(last_user_answers, column_name, current_answer)
        setattr(last_user_questions, column_name, current_question_id)
        session.commit()
        return redirect(url_for('QuizResponse', lang=lang,question_id=all_questions_ids[all_questions_ids.index(question_id)+1]))



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
