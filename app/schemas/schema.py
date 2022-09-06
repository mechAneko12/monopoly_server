from pydantic import BaseModel

class Message(BaseModel):
    message: str

class BuySpace(BaseModel):
    space_id: int
