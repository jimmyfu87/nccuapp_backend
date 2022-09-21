from fastapi import FastAPI, File, UploadFile, Request
from app.routers import example, users, card, card_relation, product, user
from app.inference import save_img, test_submit
import uvicorn
from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(users.router, prefix = '/users')
app.include_router(example.router, prefix = '/example')
app.include_router(card.router, prefix = '/card')
app.include_router(card_relation.router, prefix = '/card_relation')
app.include_router(product.router, prefix = '/product')
app.include_router(user.router, prefix = '/user')

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("Product_List.html",{"request": request})


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
