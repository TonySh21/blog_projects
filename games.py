from fastapi import APIRouter
from db.model.game import Game
from db.client import db_client
from db.schema.game import game_schema, games_schema
from bson import ObjectId

games = APIRouter()

def search_user(field: str, key):
    try:
        game = db_client.local.games.find_one({field: key})
        return Game(**game_schema(game))
    except:
        return {"Error": "No se ha encontrado el usuario"}

@games.get("/get_games", response_model=list[Game])
async def get_games():
    return games_schema(db_client.local.games.find())

@games.get("/get_game/{id}", response_model=Game)
async def get_game(id: str):
    return search_user("_id", ObjectId(id))

@games.post("/insert_game", response_model=Game, status_code=201)
async def insert_game(game: Game):
    game_dict = dict(game)
    del game_dict["id"]

    id = db_client.local.games.insert_one(game_dict).inserted_id
    new_game = game_schema(db_client.local.games.find_one({"_id":id}))

    return Game(**new_game)

@games.put("/update_game/", response_model=Game)
async def update(game: Game):
    game_dict = dict(game)
    del game_dict["id"]

    try:
        db_client.local.games.find_one_and_replace({"_id": ObjectId(game.id)}, game_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(game.id))

@games.delete("/game/{id}")
async def delete(id: str):
    found = db_client.local.games.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"Error": "No se ha eliminado el usuario"}