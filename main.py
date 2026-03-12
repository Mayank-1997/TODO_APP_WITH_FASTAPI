from fastapi import FastAPI , Request
from starlette import status
from starlette.responses import RedirectResponse

import models
from database import engine
# from routers import auth, todos, admin, users
from routers import auth , todos , admin
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static"), name = "static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url = "/todos/todo-page", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)

# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
