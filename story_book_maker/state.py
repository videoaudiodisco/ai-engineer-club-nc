from pydantic import BaseModel
from typing import List, Optional


class Page(BaseModel):
    page_number: int
    text: str
    visual_description: str
    image_url: Optional[str] = None


class PageScript(BaseModel):
    page_number: int
    script_text: str  # The specific read-aloud script for the image


class PageScriptOutput(BaseModel):
    scripts: List[PageScript]


class StoryState(BaseModel):
    theme: str
    pages: List[Page] = []
    # State will hold the scripts here once generated
    page_scripts: Optional[PageScriptOutput] = None
    status: str = "drafting"
