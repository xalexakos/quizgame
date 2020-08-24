# quizgame

A django quiz game project using questions from https://opentdb.com/

## Quick installation guide

Install python 3.8 and PIP (20.0.2)

Navigate to the projects root directory (quizgame).

Install the projects requirements (requirements.txt), preferably in a python virtualenv.  
> python3 -m venv quizegame-env

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
