from pydantic import BaseModel


class ShareModel(BaseModel):
    cluster: dict


class GetModel(BaseModel):
    token: str


