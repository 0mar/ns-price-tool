# NS price comparison

## Setup


Run `get_stations.py` to populate database with station information.
Generate a secret key and store it so `settings` can find it.
Then, start the server to find the site at `localhost:8000`. For instance:
```bash
git clone https://github.com/0mar/ns-price-tool.git
cd ns-price-tool
python3 -m venv pc_env         #|
source pc_env/bin/activate     #|Create a virtual environment; optional
pip install -r requirements.txt#|
cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1 > secret.key # Create django secret key
python manage.py migrate # Create database and models
python get_stations.py # Populate database
python manage.py runserver # Run server
```
