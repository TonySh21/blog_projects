from fastapi import APIRouter
from db.model.soft import Soft
from db.client import db_client
from db.schema.software import software_schema, softwares_schema
from bson import ObjectId

soft = APIRouter()

def search(field: str, key):
    try:
        software = db_client.local.projects.find_one({field: key})
        return Soft(**software_schema(software))
    except:
        return {"Error": "No se ha encontrado el usuario"}

@soft.get("/projects", response_model=list[Soft])
async def projects():
    return softwares_schema(db_client.local.projects.find())

@soft.get("/project/{id}", response_model=Soft)
async def project(id: str):
    return search("_id", ObjectId(id))



@soft.post("/insert_project", response_model=Soft)
async def insert(software: Soft):
    software_dict = dict(software)
    del software_dict["id"]

    id = db_client.local.projects.insert_one(software_dict).inserted_id
    new_project = software_schema(db_client.local.projects.find_one({"_id":id}))

    return Soft(**new_project)

@soft.put("/update_project", response_model=Soft)
async def update(software: Soft):
    software_dict = dict(software)
    del software_dict["id"]

    try:
        db_client.local.projects.find_one_and_replace({"_id": ObjectId(software.id)}, software_dict)
    except:
        return {"Hay un error pibe": "Solo Dios lo sabe"}

    return search("_id", ObjectId(software.id))
    
@soft.delete("/project/{id}")
async def delete(id: str):
    found = db_client.local.projects.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"Error": "No se ha eliminado el proyecto"}
