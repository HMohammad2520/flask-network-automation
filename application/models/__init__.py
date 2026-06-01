from typing import Dict, Type
from ._base import BaseModel, APIMethod
from ._db import db
from .user import User


model_map: Dict[str, Type[BaseModel]] = {
    'user': User,
}

__all__ = [
    'db',
    'BaseModel',
    'APIMethod',
    'User',
]