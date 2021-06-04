import os
import json
from hashlib import new as new_hasher
from pathlib import Path
from typing import Union
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


def get_hasher(name, data=b"", **kwargs):
    if name == "blake3":
        try:
            from blake3 import blake3
        except ImportError as exc:
            raise ImportError(
                "This function requires blake3, install with `pip install blake3`"
            ) from exc
        _kwargs = {
            k: v for k, v in kwargs.items() if k in ("key", "context", "multithreading")
        }
        return blake3(data, key=None)
    return new_hasher(name, data, **kwargs)


def path_encoder(obj: Path):
    if isinstance(obj, os.PathLike):
        return obj.__fspath__()
    # Let the base class default method raise the TypeError
    return json.JSONEncoder().default(obj)


@dataclass_json
@dataclass(frozen=True)
class Checksum(object):
    __slots__ = ["bytes", "name"]

    bytes: bytes
    name: str

    def __str__(self):
        return self.name + ":" + self.bytes.hex()

    @classmethod
    def parse(cls, cs: str):
        name, hexv = cs.split(":")
        return cls(bytes=bytes.fromhex(hexv), name=name)

    @classmethod
    def from_data(cls, data, name="blake3"):
        kwargs = {"multithreading": True} if name == "blake3" else {}
        hasher = get_hasher(name, data, **kwargs)
        return cls(bytes=hasher.digest(), name=hasher.name)

    @classmethod
    def from_path(cls, path: Union[Path, str, os.PathLike]):
        uri = Path(path)
        if not uri.is_file():
            raise FileNotFoundError("is not a file: {}".format(path))
        uri = uri.absolute()
        with open(uri, "rb") as fp:
            cs = Checksum.from_data(fp.read())
        return cls(uri=uri, checksum=cs)


@dataclass_json
@dataclass(frozen=True)
class FilePointer(object):
    #     __slots__ = ['uri', 'checksum']

    uri: Path = field(metadata=config(encoder=path_encoder))
    checksum: Checksum


@dataclass(frozen=True)
class Checksum(object):
    __slots__ = ["bytes", "name"]

    bytes: bytes
    name: str

    def __str__(self):
        """ Return colon-delimited string encoding, e.g.
        'blake3:af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262'
        """
        return self.name + ":" + self.bytes.hex()


@dataclass(frozen=True)
class NameThisDataStructure(object):
    """Represents a file or object"""
    uri: Path = field(metadata=config(encoder=path_encoder))
    size: int
    checksum: Checksum
