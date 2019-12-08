import os
import re
from pymongo import MongoClient, TEXT
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from bson.json_util import dumps, loads
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
client = MongoClient(os.getenv('MONGO_URL'))
db = client.pokedex
db.categories.create_index([("name", 1)], unique=True)


def json_helper(result, status):
    return app.response_class(
        response=dumps(result),
        status=status,
        mimetype='application/json'
    )

@app.route('/ping', methods=['GET'])
def ping():
    message = {"message": "pong"}
    return json_helper(message, 200)

@app.route('/pokemon', methods=['GET'])
def get_pokemon():
    offset = request.args.get("offset") or 0
    key = request.args.get("key") or ''
    regex = re.compile(key, re.IGNORECASE)
    query = {"ThumbnailAltText": {"$regex": regex}}
    result = db.pokemon.find(query).sort("id", 1).skip(int(offset)).limit(10)
    return json_helper(result, 200)

@app.route('/categories', methods=['GET'])
def get_categories():
    result = db.categories.find({}, {"name": 1})
    return json_helper(result, 200)

@app.route('/category/<name>', methods=['GET'])
def get_category(name):
    result = db.categories.find_one({"name": name})
    return json_helper(result, 200)


@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data["name"]
    monsters = data["pokemons"]
    result = dumps(db.pokemon.find({"id": {"$in": monsters}}).sort("id", 1))
    try:
        db.categories.insert_one({"name": name, "pokemons": loads(result)})
        result = {"message": "Duplicate category"} 
        return json_helper(result, 200)
    except:
        result = {"message": "Duplicate category"}
        return json_helper(result, 400)

@app.route('/category', methods=['PUT'])
def edit_category():
    data = request.get_json()
    name = data["name"]
    monsters = data["pokemons"]
    pokemons = dumps(db.pokemon.find({"id": {"$in": monsters}}))
    try:
        db.categories.update_one({"name": name}, {"$addToSet": {"pokemons": {"$each": loads(pokemons)}}})
        result = {"message": "Successfully updated"}
        return json_helper(result, 200)
    except:
        result = {"message": "Error in updating"}
        return json_helper(result, 400)

@app.route('/category/reorder', methods=['PUT'])
def reorder_category():
    data = request.get_json()
    name = data["name"]
    monsters = data["pokemons"]
    result = {"message": "Successfully updated"}
    try:
        db.categories.update_one({"name": name}, {"$set" :{"pokemons": monsters}})
        result = {"message": "Successfully updated"}
        return json_helper(result, 200)
    except:
        result = {"message": "Error in updating"}
        return json_helper(result, 400)

@app.route('/category/<name>', methods=['DELETE'])
def delete_category(name):
    try:
        db.categories.delete_one({"name": name})
        result = {"message": "Successfully updated"}
        return json_helper(result, 200)
    except:
        result = {"message": "Error in updating"}
        return json_helper(result, 400)



if __name__ == "__main__":
    app.run(debug=True)