release: sh -c 'cd Django\ application/project/ && python manage.py migrate'
web: sh -c 'cd Django\ application/project/ && gunicorn project.wsgi --log-file -'
