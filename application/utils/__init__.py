from typing import TypeAlias, Callable, List, Any
from ._normalizer import bool_normalizer

Normalizer: TypeAlias = Callable[[str,], Any]
Validator: TypeAlias = Callable[[Any,], bool]
Converter: TypeAlias = Callable[[Any,], Any]

normalizers: List[Normalizer] = [
    bool_normalizer,
]
Validators: List[Validator] = []
converters: List[Converter] = []


__all__ = [
    'Normalizer',
    'normalizers',
    'Validator',
    'Validators',
    'Converter',
    'converters',

    'bool_normalizer',
]
