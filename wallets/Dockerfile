FROM python:3.8.5
WORKDIR /code
COPY ./requirements.txt .
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install -r requirements.txt
COPY ./ .
CMD gunicorn wallets.wsgi:application --bind 0.0.0.0:8000
