from pydantic import BaseModel


def from_orm(schema: BaseModel,  obj):
    return schema.from_orm(obj)


class BaseScheme(BaseModel):

    class Config:
        orm_mode = True
