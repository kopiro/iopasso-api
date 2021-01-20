FROM python:3-alpine
RUN pip install pipenv
WORKDIR /usr/local/app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY ./src /usr/local/app/src
ENV FLASK_APP "src/main.py"
ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0", "--port=80" ]
EXPOSE 80