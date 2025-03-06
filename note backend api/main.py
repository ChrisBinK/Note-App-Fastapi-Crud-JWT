from fastapi import FastAPI
from routers import users, notes


app = FastAPI()

#import the user module
app.include_router(users.router)
app.include_router(notes.router)

@app.get('/')
async def index():
    return {'message': 'Index api'}