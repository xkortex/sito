from typing import Callable
from sito.datatypes import SitoMinorType, SitoMajorType, SitoMinorTypeDict

_stringly_set = frozenset({str, bytes})
_number_set = frozenset({int, float, complex})
_boolish_set = frozenset({bool, type(None)})


def get_sito_groups(o):
    typ = type(o)
    maj = SitoMinorTypeDict.get(typ, None)
    if maj is not None:
        return maj

    if typ is type:
        module = o.__module__
        name = o.__name__
        typ = o
    else:
        module = o.__class__.__module__
        name = o.__class__.__name__
        typ = type(o)

    mroset = set(typ.__mro__)

    if mroset.intersection({str, bytes}):
        #         print(mroset.intersection({str, bytes}))
        maj = SitoMajorType.STRINGLY
    elif mroset.intersection({int, float, complex}):
        maj = SitoMajorType.NUMBER
    elif mroset.intersection({list, dict, tuple, set}):
        maj = SitoMajorType.CONTAINER
    elif module in ['numpy', 'scipy', 'pandas', 'sklearn']:
        maj = SitoMajorType.BIGCONTAINER
    elif isinstance(o, Callable):
        maj = SitoMajorType.UNMARSHALLABLE
    else:
        maj = SitoMajorType.UNKNOWN

    return maj
