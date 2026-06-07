from sqlalchemy import Table, Column, Integer, Boolean, Text
from sqlalchemy.orm import Mapper
from typing import Any, Optional, List, Any
from ._db import db

class APIMethod:
    def __init__(
        self,
        request_methods: Optional[List[str]] = None,
        require_auth: bool = True,
    ):
        self.request_methods = request_methods or ['GET']
        self.require_auth = require_auth

    def __call__(self, func) -> Any:
        func._is_api_method = True
        func._request_methods = self.request_methods
        func.require_auth = self.require_auth
        return func

    @classmethod
    def is_api_method(cls, func):
        if not callable(func):
            return False

        return hasattr(func, '_is_api_method')

    @classmethod
    def get_method(
        cls,
        obj: Any,
        name: str,
        raise_error: bool = False,
        default: Any = None
    ) -> Any | None:
        func = getattr(obj, name, None)

        if not cls.is_api_method(func):
            if raise_error:
                raise AttributeError(
                    f'Attribute does not exists or is not a valid APIMethod: {func}'
                )

            return default

        return func

    @classmethod
    def get_request_methods(cls, func):
        return getattr(func, '_request_methods')

class BaseModel(db.Model):
    __table__: Table
    __mapper__: Mapper
    __abstract__ = True

    id = Column(Integer(), primary_key=True)
    description = Column(Text(), nullable=True)
    deleted = Column(Boolean(), default=False)
    readble = Column(Boolean(), default=False)
    deletable = Column(Boolean(), default=True)
    updatable = Column(Boolean(), default=True)

    def to_dict(self):
        result = {}
        columns = self.__table__.columns.keys()

        for column in columns:
            result[column] = getattr(self, column)

        return result

    @classmethod
    @APIMethod(request_methods=['GET', 'POST'])
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        db.session.add(instance)
        db.session.commit()

        return {'id': instance.id}

    @classmethod
    @APIMethod(request_methods=['GET'])
    def get_all(cls):
        return [instance.to_dict() for instance in cls.query.all()]

    @APIMethod(request_methods=['GET'])
    def get(self):
        return self.to_dict()

    @APIMethod(request_methods=['GET', 'PUT'])
    def update(self, force=False, **kwargs):
        if not bool(self.updatable) and not force:
            raise PermissionError(f'This object is readonly: {self}')

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise AttributeError(f'')

            if not isinstance(getattr(self, k), Column):
                raise AttributeError(f'')

            setattr(self, k, v)

        db.session.add(self)
        db.session.commit()

        kwargs = {k: getattr(self, k) for k in kwargs.keys()}
        kwargs.update(id=self.id)

        return kwargs

    @APIMethod(request_methods=['DELETE'])
    def delete(self, force=False, eager=False):
        if not bool(self.deletable) and not force:
            raise PermissionError(f'This object can not be deleted: {self}')

        id = self.id
        if not eager:
            self.update(deleted=True)

        else:
            db.session.delete(self)

        db.session.commit()

        return {'id': id}

    @classmethod
    @APIMethod()
    def fields(cls):
        return {
            'columns': [
                {
                    'name': col.name,
                    'type': str(col.type),
                    'nullable': col.nullable,
                    'primary_key': col.primary_key,
                    'default': str(col.default) if col.default else None
                }
                for col in cls.__table__.columns
            ],
            'relationships': [
                {
                    'name': rel.key,
                    'type': 'many-to-one' if not rel.uselist else 'one-to-many',
                    'target': rel.mapper.class_.__name__
                }
                for rel in cls.__mapper__.relationships
            ]
        }

    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id})'

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, '__tablename__'):
            raise RuntimeError(
                f'Model `{cls.__name__}` should have `__tablename__` attribute.'
            )

        return super().__init_subclass__()
