from fastapi import FastAPI
import routers.games as games
import routers.software as software

app = FastAPI()
app.include_router(games.games)
app.include_router(software.soft)

@app.get("/")
async def home_page():
    return "Welcome to Game Store and Projects from Tony"