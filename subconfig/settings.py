from typing import Optional, Union, Tuple, Mapping
from pathlib import Path
import json

from .typing import PathLike

_PROPERTIES = "_properties"
_FILE = "_file"


class PropertyValueSetError(Exception):
    pass


class PropertyValueChoice(PropertyValueSetError):
    pass


class Property:
    def __init__(self, name: str, default: Optional[Union[str, bool]] = None, choices: Optional[Tuple] = None):
        assert isinstance(name, str), f"invalid add_property(name=value, ...) value type!"
        self._name = name
        self._choices = choices
        self._value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if self._choices:
            if v not in self._choices:
                raise PropertyValueChoice(f"illegal '{self._name}' property value: '{v}' (choices: {self._choices})")
        self._value = v

    def __repr__(self):
        return f"Property({self._name}={self._value})"


class Settings:
    def __init__(self, file: PathLike):
        """Settings represent a one-dimensional dictionary of properties for which you can change values"""
        self.__dict__[_FILE] = Path(file)
        self.__dict__[_PROPERTIES] = {}
    
    def _attr(self, name: str):
        """access attribute 'name' without triggering __getattr__ magic to avoid infinite recursion"""
        return self.__dict__[name]

    def __getattr__(self, item):
        _properties = self._attr(_PROPERTIES)

        if item in _properties.keys():
            return _properties.get(item)
        else:
            super().__getattribute__(item)

    def __setattr__(self, key, value):
        print(f"property {key} set with value {value}")
        _properties = self._attr(_PROPERTIES)

        if key in _properties.keys():
            p = _properties.get(key)
            if p:
                p.value = value
                self._update_file(self.get_as_dict())
        else:
            raise PropertyValueSetError("you can only set attributes that were defined with add_property(...) method")

    def __repr__(self):
        _properties = self._attr(_PROPERTIES)

        return f"Settings({self.get_as_dict()})"

    def get_as_dict(self):
        _properties = self._attr(_PROPERTIES)

        return {k: p.value for k, p in _properties.items()}

    def _update_file(self, d: Mapping):
        with open(self._file, mode="w+") as fp:
            json.dump(d, fp)

    def add_property(self, name: str, default=None, type=str, choices: Optional[Tuple] = None):
        """create new settings property"""
        _properties = self._attr(_PROPERTIES)

        assert name not in self._properties.keys(), f"property named {name} already exits!"
        _type_choices = str, bool
        assert type in _type_choices, f"invalid 'add_property(type=value, ...) (choices: {_type_choices})"

        _choices = choices

        if isinstance(type, bool):
            _choices = (True, False, )

        _properties[name] = Property(name=name, default=default, choices=_choices)
