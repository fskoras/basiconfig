"""Configuration management library"""

import os.path
import re
from typing import List, Dict, Tuple, Union, Optional, MutableMapping
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

    # retrieve value
    val = d.get(k)

    # just return if not a string
    if not isinstance(val, str):
        return val

    def _interpolate_util(val: str, d: MutableMapping):
        for match in _INTERPOLATION_PATTERN.finditer(val):
            old = match.group(0)
            key = old.strip(r"${}")
            new = d.get(key)

            types_allowed = (str, int, float, )
            if not any(isinstance(new, t) for t in types_allowed):
                SubConfigError("Only string or numeric value interpolation allowed")

            new_val = val.replace(old, new)
            return _interpolate_util(new_val, d)
        return val

    val = _interpolate_util(val, d)

    return val


class SubConfig(object):
    def __init__(self, files: List[_PathLike]):
        """configuration files will be loaded in supplied order"""
        self._config_raw: Dict[Path, MutableMapping] = self._load_config_files_raw(files)

    def __getitem__(self, item):
        # TODO: dynamic loading of config values from multiple files
        fd = FlatterDict({}, delimiter=_DELIMITER)

        for v in self._config_raw.values():
            fd.update(FlatterDict(v, delimiter=_DELIMITER))

        # resolve item value interpolation
        result = _interpolate(fd, item)

        return result

    def __repr__(self):
        """show loaded configuration files"""
        return f"BasiConfig({[f.name for f in self._config_raw.keys()]})"

    @staticmethod
    def _read_config_file(file: _PathLike) -> Optional[Tuple[Path, str]]:
        """check configuration files validity and return (Path, Content) pair"""

        if not os.path.exists(file):
            _log.warning("configuration file does not exist: " + str(file))
            return None
        else:
            with open(file, mode="r", encoding="utf-8") as fp:
                return Path(file).resolve(), fp.read()

    @staticmethod
    def _json_to_dict(s) -> MutableMapping:
        import json
        return json.loads(s)

    def _load_config_files_raw(self, files: List[_PathLike]) -> Dict[Path, MutableMapping]:
        """"""
        store = {}

        for file in files:
            result = self._read_config_file(file)
            if result:
                file, content = result

                if file.suffix.lower() == ".json":
                    d = self._json_to_dict(content)
                    store[file] = d

        return store
