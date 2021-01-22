from datetime import timedelta

class Config:
    DEBUG = True
    BASE_URL = "http://127.0.0.1:5000"
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'random-string'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds = 120)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True

# Random string
# grc.com 
# Services/Perfect Passwords