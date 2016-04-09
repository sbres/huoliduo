#!/bin/bash

NAME="holido_api"                                  # Name of the application
APPDIR=/work/Backend/holido       					# Django project directory
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn

# Activate the virtual environment
cd $APPDIR
source ../virtual_env/bin/activate
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn main:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind 0.0.0.0:8000
