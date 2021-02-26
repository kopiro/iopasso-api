#!/bin/sh
flask db upgrade
gunicorn --pythonpath ./src --access-logfile - --bind 0.0.0.0:80 app:app