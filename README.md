# Pokedex backend

Built using python, powered by Flask

## Instrutions on running

* Clone the repo
* Install mongodb if you does not have it
* Create an `.env` file and add `MONGO_URL=<MONGO URI>`

```
curl https://5n6ugc33m6.exe;2C;2Ccute-api.us-east-1.amazonaws.com/api/pokedex -o pokedex.json
mongoimport --db pokedex --collection pokemon --file pokedex.json --jsonArray
pip install -r requirements.txt
python app.py
```