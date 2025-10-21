from pydantic import BaseModel, AnyHttpUrl

class InUrl(BaseModel):
    large_url: AnyHttpUrl
    
class OutUrl(InUrl):
    tiny_url: str