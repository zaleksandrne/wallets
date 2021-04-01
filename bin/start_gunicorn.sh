source /home/alex/code/wallets/env/bin/activate
exec gunicorn -c "/home/alex/code/wallets/wallets/gunicorn_config.py" wallets.wsgi
