import os

bind = "0.0.0.0:8888"
workers = 4

errorlog = os.path.join(os.getcwd(), 'logs', 'gunicorn_error.log')
loglevel = 'info'
accesslog = os.path.join(os.getcwd(), 'logs', 'gunicorn_access.log')