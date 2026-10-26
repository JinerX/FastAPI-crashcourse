from fastapi import FastAPI

api = FastAPI()

# GET POST PUT DELETE - primary HTTP methods
@api.get('/')
def index():
    return "Hello world"


@api.get('/json')
def index():
    return {"message" :"Hello world"}
