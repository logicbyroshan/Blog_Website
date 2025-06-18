#!/usr/bin/env bash
# exit on error
set -o errexit

# Install project dependencies
pip install -r requirements.txt

# Run Django's deployment commands
python manage.py collectstatic --no-input
python manage.py migrate

# --- ADD THIS LINE ---
# Run our custom command to create the superuser
python manage.py createsu