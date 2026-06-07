from typing import Dict, Type
from ._base import BaseModel, APIMethod
from ._db import db
from .user import User
from .script import Script
from .context import Context

model_map: Dict[str, Type[BaseModel]] = {
    'user': User,
    'script': Script,
    'context': Context,
}

__all__ = [
    'db',
    'BaseModel',
    'APIMethod',
    'User',
    'Script',
]