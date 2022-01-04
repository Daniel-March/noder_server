import json
import random
import string

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import *
from fastapi.responses import Response

import settings
from data_models import *
from database import Database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/share")
def share(data: ShareModel):
    database = Database()
    token = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    while database.get("cluster", where={"token": token}) is not None:
        token = [random.choice(string.ascii_letters + string.digits) for _ in range(32)]
    data.cluster["token"] = token
    database.set("cluster", data.cluster)
    return Response(status_code=200, content=token)


@app.post("/get")
def get(data: GetModel):
    database = Database()
    cluster = database.get("cluster", where={"token": data.token})
    if cluster is not None:
        del cluster["token"]
        return Response(status_code=200, content=json.dumps(cluster))
    return Response(status_code=400)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
