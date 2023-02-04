"""Configuration management library"""

import os.path
import re
from typing import List, Tuple, Union, Optional, Mapping, MutableMapping
from pathlib import Path
import logging as _log

from flatdict import FlatterDict

# constants
_DELIMITER = '.'
_INTERPOLATION_PATTERN = re.compile("\$\{[\w\.]+\}")

# custom typing
_PathLike = Union[str, os.PathLike]


class SubConfigError(Exception):
    ...


def _interpolate(d: MutableMapping, k: str):
    """Resolve item value interpolation

    :param d: configuration dictionary context
    :param k: key for d value to be resolved
    :return: expanded value
    """
    # retrieve value
    val = d.get(k)

    # just return if not a string
    if not isinstance(val, str):
        return val

    def _interpolate_util(val: str, d: MutableMapping):
        """Recursive value key resolver"""
        for match in _INTERPOLATION_PATTERN.finditer(val):
            old = match.group(0)
            key = old.strip(r"${}")
            new = d.get(key)

            types_allowed = (str, int, float, )
            if not any(isinstance(new, t) for t in types_allowed):
                SubConfigError("Only string or numeric value interpolation allowed")

            new_val = val.replace(old, str(new))
            return _interpolate_util(new_val, d)
        return val

    val = _interpolate_util(val, d)

    return val


class Config:
    def __init__(self, d: Mapping, file: _PathLike = None):
        """Abstraction for easier multiple configuration files management"""
        self._file = Path(file)
        self._config: Mapping = FlatterDict(d, delimiter=_DELIMITER)

    @property
    def file(self) -> Optional[Path]:
        return self._file

    @property
    def data(self) -> Mapping:
        return self._config

    @staticmethod
    def _read_config_file(file: _PathLike) -> Optional[str]:
        """Check configuration files validity and return (Path, Content) pair"""

        if not os.path.exists(file):
            _log.warning("configuration file does not exist: " + str(file))
            return None
        else:
            with open(file, mode="r", encoding="utf-8") as fp:
                return fp.read()

    @classmethod
    def from_json_file(cls, p: _PathLike):
        p = Path(p).resolve()
        s = cls._read_config_file(p)
        if s:
            from json import loads
            return cls(loads(s), file=p)


class SubConfig:
    def __init__(self, files: Union[_PathLike, List[_PathLike]]):
        """Configuration files will be loaded in supplied order"""

        # let's be forgiving and support single file input as well
        if isinstance(files, _PathLike):
            files = [files]

        self._config: List[Config] = self._load_files_to_config(files)

    def __getitem__(self, item):
        fd = FlatterDict({}, delimiter=_DELIMITER)

        # join all configurations to allow shared values interpolation between files
        for config in self._config:
            fd.update(config.data)

        result = _interpolate(fd, item)

        return result

    def __repr__(self):
        """Show loaded configuration files"""
        return f"BasiConfig({[f.file.name for f in self._config]})"

    @staticmethod
    def _load_files_to_config(files: List[_PathLike]) -> List[Config]:
        """Internal config files loader"""
        store = []

        for file in files:
            f = Path(file)
            suffix = f.suffix

            # match file suffix to Config loader
            if suffix.lower() == ".json":
                store.append(Config.from_json_file(f))
            else:
                SubConfigError(f"Unsupported file extension: {suffix}. Unable to detect file type: {f.name}")

        return store
