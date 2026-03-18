from pydantic import BaseModel
from typing import List, Optional


class Page(BaseModel):
    page_number: int
    text: str
    visual_description: str  # The "Image Explainer" output lives here
    image_url: Optional[str] = None


class StoryState(BaseModel):
    theme: str
    pages: List[Page] = []
    status: str = "drafting"
