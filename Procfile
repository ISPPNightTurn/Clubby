release: sh -c 'cd djangoapp && python manage.py migrate'
web: sh -c 'cd djangoapp && gunicorn project.wsgi --log-file -'
