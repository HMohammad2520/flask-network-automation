from ._base import BaseModel
from sqlalchemy import Column, VARCHAR
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    first_name = Column(VARCHAR(254), unique=False, nullable=True)
    last_name = Column(VARCHAR(254), unique=False, nullable=True)
    email = Column(VARCHAR(254), unique=True, nullable=False)
    username = Column(VARCHAR(254), unique=True, nullable=False)
    password = Column(VARCHAR(254), nullable=False)

    @property
    def full_name(self) -> str:
        return f'{self.first_name or ''
        }{
            ' ' if all((self.first_name, self.last_name)) else ''
        }{
            self.last_name or ''
        }'.title() or str(self.username)
