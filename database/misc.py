# In this file we will store some function which requires
# usage of several repos to simplify DB interaction.
from fastapi import HTTPException

from .repo.requests import RequestsRepo

