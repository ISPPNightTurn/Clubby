ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    # 'clubby',
]

BASEURL = 'http://localhost:8000'

APIS = {
    'clubby': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clubby',
        'USER': 'clubby',
        'PASSWORD': 'clubby',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
