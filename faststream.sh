#!/bin/bash

cd backend
python manage.py migrate
faststream run serve_faststream:app
