from fastapi import FastAPI, File, UploadFile, Request
from app.routers import example, card, card_relation, product, user
import uvicorn
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# app.include_router(example.router, prefix = '/example')
# app.include_router(card.router, prefix = '/card')
# app.include_router(card_relation.router, prefix = '/card_relation')
app.include_router(product.router, prefix = '/product')
app.include_router(user.router, prefix = '/user')

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse('Login.html')


@app.get("/Login.html")
def login_view(request: Request):
    return templates.TemplateResponse("Login.html",{"request": request})


@app.get("/Register.html")
def register_view(request: Request):
    return templates.TemplateResponse("Register.html",{"request": request})


if __name__ == '__main__':
    uvicorn.run(app = 'main:app', host = '127.0.0.1' , port = 9191, reload= True, debug = True)
