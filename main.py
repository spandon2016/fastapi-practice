from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from exceptions import StoryException
from router import blog_get
from router import blog_post
from router import user
from router import article 
from router import product, file
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication 
from fastapi.staticfiles import StaticFiles

# 56 2:17 9/19/23

app = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

# alt shift F for formatting
# ctrl k , ctrl s

@app.get("/hello")
def index():
    return {"message": "Hello World"}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name }

    )

# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.mount('/files', StaticFiles(directory="files"), 
          name='files')