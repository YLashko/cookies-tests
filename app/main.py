from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    cookies = [
        {
            "name": key,
            "value": val
        }
        for key, val in request.cookies.items()
    ]

    return templates.TemplateResponse(
        request=request,
        name="main.html.jinja",
        context={"cookies": cookies}
    )


@app.get("/none-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    response = RedirectResponse("/")
    response.set_cookie("samesite_none", value=value, secure=True, samesite='none', httponly=True)
    return response


@app.get("/lax-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    response = RedirectResponse("/")
    response.set_cookie("samesite_lax", value=value, secure=True, samesite='lax', httponly=True)
    return response


@app.get("/strict-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    response = RedirectResponse("/")
    response.set_cookie("samesite_strict", value=value, secure=True, samesite='strict', httponly=True)
    return response


@app.get("/none-cookie/")
def set_cookie_none(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("samesite_none", secure=True, httponly=True)
    return response


@app.get("/lax-cookie/")
def set_cookie_none(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("samesite_lax", secure=True, httponly=True)
    return response


@app.get("/strict-cookie/")
def set_cookie_none(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("samesite_strict", secure=True, httponly=True)
    return response
