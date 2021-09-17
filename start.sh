pip3 install -r requirements.txt
python3 setup.py
python3 manage.py migrate
python3 manage,py loaddata data.json --app interact