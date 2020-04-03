release: sh -c 'cd Django_app && python manage.py migrate'
web: sh -c 'cd Django_app && gunicorn project.wsgi --log-file -'
