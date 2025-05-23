from .projects import projects_router
from .users import users_router
from .orders import orders_router

routers_list = [
    projects_router,
    users_router,
    orders_router,
]
