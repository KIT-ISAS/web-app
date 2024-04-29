ssh isas-interactive

sudo apt update
sudo apt install git
sudo apt install virtualenv

rm ./web-app
git clone https://github.com/KIT-ISAS/web-app.git
cd ./web-app
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Python Environment (shouldn't be used on production server, but has debug messages)
nohup python app.py &

# Official production solution
# gunicorn --bind localhost:8050 app:server

# http://193.196.38.30:8080

# ps
# pkill -9 python
