# Usage on Server:
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Python Environment (shouldn't be used on production server, but has debug messages)
python app.py


# gunicorn --bind localhost:8050 app:server


