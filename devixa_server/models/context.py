# models/context_model.py
from sqlalchemy import Column, String, JSON, Boolean
from ._base import BaseModel


class Context(BaseModel):
    __tablename__ = 'contexts'

    name = Column(String(255), nullable=False, index=True)
    context_data = Column(JSON, nullable=False, default={})
    is_default = Column(Boolean, default=False)
