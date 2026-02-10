#!/bin/bash
python app.py
# uwsgi --ini uwsgi.ini

#gunicorn -w 4 --threads 2 -b 0.0.0.0:8000 app:server