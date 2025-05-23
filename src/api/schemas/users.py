from enum import Enum
from pydantic import BaseModel

from schemas.projects import ProjectResponse

    
class ProjectCart(BaseModel):
    project_id: int
    extra: list[dict]
    main: dict
    
class ProjectCartResponse(BaseModel):
    project_id: int
    extra: list[dict]
    main: str
    category: str
    quantity: int
    price: int
    icon_url: str
    subscribers: int
    views: int
    name: str
    type: str | None = None
    
class ProjectCartDelete(BaseModel):
    project_id: int
    main: str   

class UserCart(BaseModel):
    projects: list[ProjectCartResponse] # список проектов в корзине
    quantity: int # количество проектов в корзине
    subtotal: int # сумма заказа
    discount: int # скидка
    total: float # общая сумма заказа


"""
data add project to cart:
    
    id - project_id
    extra - list of formats (в ТГ: он всегда один (1/24 или 2/48); в инстаграм: Слайды в сторис, соавторство или шапка)
    main - "Публикация" / "Сторис"

    {
        "projects": {
            "id": 1,
            "main": "Публи кация" / "Сторис",
            "category": "telegram" / "instagram",
            "price": 1000,
            "extra": [
                { 
                    "name": "1/24",
                    "price": 1000
                },
                {
                    "name": "Сторис в слайды",
                    "price": 1000
                }
            ],
        }
    }


"""