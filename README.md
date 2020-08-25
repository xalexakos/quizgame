# quizgame

A django quiz game project using questions from https://opentdb.com/

## Quick installation guide

Install python 3.8 and PIP (20.0.2)

Navigate to the projects root directory (quizgame).

Install the projects requirements (requirements.txt), preferably in a python virtualenv.  
> python3 -m venv quizgame-env

> source quizgame-env/bin/activate

> pip install -r requirements.txt  

#
The default django sqlite3 database requires no installation, just migrate the models by typing
> python manage.py migrate

To create some quizzes the following command can be used
> python manage.py createquizzes <no_of_quizzes>

For example in order to create 100 new quizzes type
> python manage.py createquizzes 100

# 
Run django server by typing
> python manage.py runserver

Access the application by typing the following url in any browser, create an account and start answering right away.
> http://127.0.0.1:8000/


## Tests 
In order to execute the tests type:
> python manage.py test --settings=tests.settings


#
# API

GET http://127.0.0.1:8000/api/quiz/ returns a random quiz in JSON format.

POST http://127.0.0.1:8000/api/quiz/ submits a quiz and returns the number of correct answers in JSON format.

GET http://127.0.0.1:8000/api/quiz/success-rate/ returns the percentage of submissions with more than 7 correct answers per quiz.