#!/bin/bash

rm db.sqlite3
rm -rf ./roadmapapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations roadmapapi
python3 manage.py migrate roadmapapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

