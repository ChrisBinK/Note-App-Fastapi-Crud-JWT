from fastapi import FastAPI
from routers import users, notes
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect

app = FastAPI()
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#import the user module
app.include_router(users.router)
app.include_router(notes.router)

@app.get('/')
async def index():
    return {'message': 'Index api'}