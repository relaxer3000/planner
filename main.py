import uvicorn
from fastapi import FastAPI

from database.connection import conn, drop_database
from routes.users import user_router
from routes.events import event_router


app = FastAPI()

app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix="/events")


@app.on_event('startup')
def on_startup():
    conn()


@app.on_event('shutdown')
def on_shutdown():
    drop_database()


if __name__ == '__main__':
    uvicorn.run("main.app", host="127.0.0.1", port=5000, reload=True)
