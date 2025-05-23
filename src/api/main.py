import json
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import (BaseHTTPMiddleware,
                                    RequestResponseEndpoint)

from starlette.responses import Response
import uvicorn

from config import PORT, HOST

from database import get_session_pool, close_engine
from routers import routers_list

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RealIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            real_ip = x_forwarded_for.split(",")[
                0
            ]  # Берем первый IP из списка
        else:
            real_ip = request.client.host
        request.state.real_ip = real_ip
        response = await call_next(request)
        return response


app.add_middleware(RealIPMiddleware)



# init SQLAlchemy DB engine
session_pool = get_session_pool()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with session_pool() as session:
        request.state.db_session = session
        
        response = await call_next(request)
        return response

@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    await close_engine()


# Подключаем роутеры
for router in routers_list:
    app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, ssl_keyfile=f"/etc/letsencrypt/live/{HOST}/privkey.pem", ssl_certfile=f"/etc/letsencrypt/live/{HOST}/fullchain.pem") 