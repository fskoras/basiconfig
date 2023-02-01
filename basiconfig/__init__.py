"""Configuration management library"""

import os.path
from typing import List, Dict, Tuple, Union, Optional, MutableMapping
from pathlib import Path
import logging as _log

from flatdict import FlatterDict

# constants
_DELIMITER = '.'

# custom typing
_PathLike = Union[str, os.PathLike]


class BasiConfig(object):
    def __init__(self, files: List[_PathLike]):
        """configuration files will be loaded in supplied order"""
        self._config_raw: Dict[Path, MutableMapping] = self._load_config_files_raw(files)

    def __getitem__(self, item):
        # TODO: dynamic loading of config values from multiple files
        for v in self._config_raw.values():
            return FlatterDict(v, delimiter=_DELIMITER).get(item)

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
            with open(file, mode="r") as fp:
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
