# Web programming quiz
## Python application using Flask framework

### Team Awesome! :D

* Aleksandar Ikonomov
* Mario Georgiev
* Nadejda Todorova
* Yoan Ivanov

### Instructions
1. Провери дали имаш инсталиран "virtualenv" с командата:
virtualenv --version
Aко излезне 15.0.1 например всичко е ок.Ако даде грешка трябва да го инсталираш:
(за ubuntu)
sudo apt-get install python-virtualenv

2. След това свали репозиторито на проекта ни (ако го нямаш):
git clone https://github.com/ikonomov17/Web-programming-quiz.git

3. В главната папка отвори конзолата 
(за windows: shift+дясно копче => Open command prompt /
ubuntu: дясно копче open terminal)
и въведи:
virtualenv venv

4. След тази команда вече трябва да има две папки app и venv

5. В конзолата пишеш 
ubuntu:
source venv/bin/activate
windows:
свали си убунту :D :D 

6. След това в конзолата
pip install -r requirements.txt

7. После 
export FLASK_APP=app/app.py
flask run

8. Отваряш браузъра на localhost:5000/

9. Server-a се спира от конзолата с Ctrl+Z но трябва да затвориш терминала и да повториш 5 и 7 стъпка 
