from datetime import datetime
from pydantic import BaseModel


class PostImageResponse(BaseModel):
    id: int
    image_url: str
    created_at: datetime
