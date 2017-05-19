# Web programming quiz
## Python application using Flask framework

### Team Awesome! :D

* Aleksandar Ikonomov
* Mario Georgiev
* Nadejda Todorova
* Yoan Ivanov

### Instructions
1. Провери дали имаш инсталиран "virtualenv" с командата: <br />
virtualenv --version<br />
Aко излезне 15.0.1 например всичко е ок.Ако даде грешка трябва да го инсталираш:<br />
(за ubuntu)<br />
sudo apt-get install python-virtualenv<br />

2. След това свали репозиторито на проекта ни (ако го нямаш):<br />
git clone https://github.com/ikonomov17/Web-programming-quiz.git<br />

3. В главната папка отвори конзолата <br />
(за windows: shift+дясно копче => Open command prompt /<br />
ubuntu: дясно копче open terminal)<br />
и въведи:<br />
virtualenv venv<br />

4. След тази команда вече трябва да има две папки app и venv<br />

5. В конзолата пишеш <br />
ubuntu:<br />
source venv/bin/activate<br />
windows:<br />
свали си убунту :D :D <br />

6. След това в конзолата<br />
pip install -r requirements.txt<br />

7. После <br />
export FLASK_APP=app/app.py<br />
python app/app.py<br />
Сървъра следи за промени във файловете, така че не би трябвало да го рестартирате често.<br />

8. Отваряш браузъра на localhost:5000/

9. Server-a се спира от конзолата с Ctrl+C

10. За да излезнеш от режима (env) се пише в конзолата deactivate
