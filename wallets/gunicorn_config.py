command = '/home/alex/code/wallets/env/bin/gunicorn'
pythonpath = '/home/alex/code/wallets/wallets'
bind = '127.0.0.1:8030'
workers = 3
user = 'alex'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=wallets.settings'
