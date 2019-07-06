mkvirtualenv -p /usr/bin/python3 messaging
cookiecutter https://github.com/pydanny/cookiecutter-django

CREATE USER messaging WITH ENCRYPTED PASSWORD 'messaging';
CREATE database messaging;
ALTER USER messaging CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE messaging TO messaging;