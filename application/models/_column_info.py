from typing import Optional
from ..utils import Converter, Normalizer, Validator, bool_normalizer

class ColumnInfo:
    _index = 'column_info'

    def __init__(
        self,
        converter: Optional[Converter] = None,
        validator: Optional[Validator] = None,
        normalizer: Optional[Normalizer] = None,
    ):
        self.converter = converter
        self.validator = validator
        self.normalizer = normalizer

    def to_dict(self):
        return {
            self._index: self,
            'convertor': self.converter,
            'validator': self.validator,
            'normalizer': self.normalizer,
        }

base_info = ColumnInfo()
id_info = ColumnInfo(converter=int)
name_info = ColumnInfo(converter=str.title)
username_info = ColumnInfo()
bool_info = ColumnInfo(normalizer=bool_normalizer)