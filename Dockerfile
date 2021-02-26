FROM python:3.9-alpine

ENTRYPOINT [ "/bin/entrypoint" ]
WORKDIR /usr/local/app
EXPOSE 80
ENV FLASK_APP ./src/app.py
ENV FLASK_ENV "production"

RUN apk --no-cache add musl-dev gcc libffi-dev

RUN pip install --no-cache-dir pipenv==2020.11.15
COPY Pipfile Pipfile.lock ./
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /bin/entrypoint
COPY ./migrations ./migrations
COPY ./src ./src