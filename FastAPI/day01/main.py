from fastapi import FastAPI

app = FastAPI()

# define endpoint
@app.get("/")
def hello():
    return {'message': 'Hello, FastAPI!'}
# To run the application, use the command:
# uvicorn main:app --reload


@app.get('/about')
def about():
    return {'message': 'This is a FastAPI application.'}
