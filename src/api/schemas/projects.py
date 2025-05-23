from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Category(str, Enum):
    telegram = "telegram"
    instagram = "instagram"

class SortOrder(str, Enum):
    none = "none"
    ascending = "ascending"
    descending = "descending"

class ProjectType(str, Enum):
    all_projects = "all_projects"
    hot = "hot"
    new = "new" 
    discount = "discount"

class ProjectBase(BaseModel):
    id: int
    status: str
    category: str
    business_details: dict
    view_details: dict
    price: dict
    count_favorites: int
    created_at: datetime
    subscribers: int
    views: int
    name: str
    is_favorite: bool
    type: str | None = None

class ProjectResponse(ProjectBase):
    pass

class ProjectsListResponse(BaseModel):
    message: str
    data: List[ProjectResponse]  # List of projects
    
    new_projects: List[ProjectResponse]  # List of new projects
    hot_projects: List[ProjectResponse]  # List of hot projects
    
    bots_tg: List[ProjectResponse]  # List of bots
    channels_tg: List[ProjectResponse]  # List of channels
