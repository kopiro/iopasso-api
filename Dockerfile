FROM python:3-alpine

ENTRYPOINT [ "/bin/entrypoint" ]

ENV FLASK_APP ./src/app.py
WORKDIR /usr/local/app
EXPOSE 80

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY ./entrypoint.sh /bin/entrypoint
COPY ./migrations /usr/local/app/migrations
COPY ./src /usr/local/app/src