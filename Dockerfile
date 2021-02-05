FROM python:3-alpine

ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0", "--port=80" ]
WORKDIR /usr/local/app
ENV FLASK_APP "src/main.py"
EXPOSE 80

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY ./src /usr/local/app/src
RUN flask db upgrade