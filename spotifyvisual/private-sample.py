import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_settings = {
    # sqlite for local development
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # or postgres for production
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spotifyvisual',
        'USER': 'spotifyvisual',
        'PASSWORD': '5p0tIfYf0Rth3w1n',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }   
}

spotify_keys = { 
    'CLIENT_ID': 'put your spotify client id here',
    'CLIENT_SECRET': 'put your spotify client secret here',
    'REDIRECT_URI': 'http://localhost:8000/callback',
}
