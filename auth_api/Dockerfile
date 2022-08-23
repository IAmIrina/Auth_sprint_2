FROM python:3.10-buster

RUN  groupadd -r runner --gid=1280 && useradd -r -g runner --uid=1280 --create-home --shell /bin/bash runner

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

COPY ./src /home/runner/
USER runner
WORKDIR /home/runner

# CMD  python3 wait_for_postgres.py && python3 pywsgi.py 

CMD gunicorn --worker-class gevent \
    --workers $WORKERS \
    --bind 0.0.0.0:9001 \
    wsgi_app:app

EXPOSE $AUTH_API_PORT