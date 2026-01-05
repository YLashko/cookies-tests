from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://online4.superoffice.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Content-Security-Policy"] = "frame-ancestors https://online4.superoffice.com"
    return response


class PartitionedCookieRedirectResponse(RedirectResponse):
    def set_partitioned_cookie(
        self,
        key: str,
        value: str,
        max_age: int = None,
        httponly: bool = True,
    ):
        cookie = f"{key}={value}; Path=/; Secure; SameSite=None; Partitioned"
        if httponly:
            cookie += "; HttpOnly"
        if max_age:
            cookie += f"; Max-Age={max_age}"
        
        self.headers.append("Set-Cookie", cookie)


@app.get("/")
def home(request: Request):
    tiid = ""
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
        context={
            "cookies": cookies,
            "tiid": tiid
        }
    )


@app.get("/ticket/{tiid}")
def home(request: Request, tiid: int):
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
        context={
            "cookies": cookies,
            "tiid": tiid
        }
    )


@app.get("/none-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = PartitionedCookieRedirectResponse(redirect_to)
    # response.set_cookie("samesite_none", value=value, secure=True, samesite='none', httponly=True)
    response.set_partitioned_cookie(
        key="samesite_none",
        value=value,
        httponly=True,
        # httponly=False,
        max_age=60*60*24
    )
    return response


@app.get("/lax-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = RedirectResponse(redirect_to)
    response.set_cookie("samesite_lax", value=value, secure=True, samesite='lax', httponly=True)
    # response.set_partitioned_cookie(
    #     key="samesite_lax",
    #     value=value,
    #     max_age=60*60*24
    # )
    return response


@app.get("/strict-cookie/{value}")
def set_cookie_none(request: Request, value: str):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = RedirectResponse(redirect_to)
    response.set_cookie("samesite_strict", value=value, secure=True, samesite='strict', httponly=True)
    return response


@app.get("/none-cookie/")
def set_cookie_none(request: Request):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = RedirectResponse(redirect_to)
    response.delete_cookie("samesite_none", secure=True, httponly=True, samesite='none')
    return response


@app.get("/lax-cookie/")
def set_cookie_none(request: Request):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = RedirectResponse(redirect_to)
    response.delete_cookie("samesite_lax", secure=True, httponly=True)
    return response


@app.get("/strict-cookie/")
def set_cookie_none(request: Request):
    redirect_to = request.query_params.get("redirect_to", "/")
    response = RedirectResponse(redirect_to)
    response.delete_cookie("samesite_strict", secure=True, httponly=True)
    return response
