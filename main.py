from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form
from app.routers import example, users
from app.inference import save_img, test_submit
import uvicorn
from starlette.responses import FileResponse 

app = FastAPI()
app.include_router(users.router, prefix = '/users')
app.include_router(example.router, prefix = '/example')

@app.get("/")
def root():
    return FileResponse('index.html')

@app.post("/predict", tags=["predict"])
async def prediction(file: UploadFile = File(...)):
    file_name = save_img(file)
    result = test_submit(file_name)
    if result[0]==1:
        return  {"answer": "dog"}
    elif result[0]==0:
        return  {"answer": "cat"}
    else:
        return  'Result is wrong!!'


if __name__ == '__main__':
    uvicorn.run(app = 'main:app', host = '127.0.0.1' , port = 8080, reload= True, debug = True)
