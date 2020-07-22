# NS price comparison

## Setup


Run `get_stations.py` to populate database with station information.
Generate a secret key and store it so `settings` can find it.
Then, start the server to find the site at `localhost:8000`. For instance;
```bash
python get_stations.py
cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1 > secret.key
python manage.py runserver
``` 
