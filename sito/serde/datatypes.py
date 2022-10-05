from typing import Callable
from collections import Mapping
from enum import Enum


class SitoMajorType(Enum):
    """
    There's basically a few loose groups of interfaces to deal with, which determine serialization behavior

    Unknown - what it says on the tin
    UNMARSHALLABLE - Something Sito cannot hash. Complex datatypes which do not have an obvious marshalling strategy
    STRINGLY - Because str, bytes and tuple implement very similar interfaces, we want to catch these first and
        deal with them separately.
    CONTAINER - Implements Container or Sequence. Has a finite length
    BIGCONTAINER - A container that is difficult to serialize. This includes numpy.ndarray, pd.DataFrame, and similar
        Serialization is possible but not always well-defined

    """

    UNKNOWN = 'Unknown'
    NONE = 'None'
    UNMARSHALLABLE = 'Unmarshallable'
    Type = 'Type'  # classes and types
    BOOLISH = 'Boolish'  # bool and None
    STRINGLY = 'Stringly'  # str and bytes
    NUMBER = 'Number'  # numerical types
    CONTAINER = 'Container'  # Iterable. Has child nodes. Includes list, dict, set, and abstract equivalents
    BIGCONTAINER = 'BigContainer'  # A container that is difficult to serialize. Numpy arrays, pandas dataframes, models


class SitoMinorType(Enum):
    """A broad classsifaction of object types"""

    UNKNOWN = 'Unknown'
    TYPE = 'Type'
    NONE = 'None'
    CALLABLE = 'Callable'
    PRIMITIVE = 'Primitive'  # anything natively json serialisable, other than containers
    BYTES = 'Bytes'  # not json serialisable natively
    NUMBER = 'Number'  # Numbers which are json serialisable natively
    MAPPING = 'Mapping'  # a mapping style container. Ordering may not matter
    SEQUENCE = 'Sequence'  # Sequence, aside from Primitives. anything coercible to a finite list. Order is preserved
    SET = 'Set'  # A collection which cannot contain duplicates, set, dict.keys()
    ARRAY = 'Array'  # numpy array or matrix
    SERIES = 'Series'  # pd.Series
    DATAFRAME = 'Dataframe'  # pd.Dataframe
    INDEX = 'Index'  # pd.Index
    ESTIMATOR = 'Estimator'  # sklearn.base.Estimator


# for fast checking of well-known types
SitoMajorTypeDict = {
    type(None): SitoMajorType.NONE,
    type: SitoMajorType.TYPE,
    bytes: SitoMajorType.STRINGLY,
    bool: SitoMajorType.BOOLISH,
    str: SitoMajorType.STRINGLY,
    int: SitoMajorType.NUMBER,
    float: SitoMajorType.NUMBER,
    complex: SitoMajorType.NUMBER,
    dict: SitoMajorType.CONTAINER,
    list: SitoMajorType.CONTAINER,
    tuple: SitoMajorType.CONTAINER,
    set: SitoMajorType.CONTAINER,
}

SitoMinorTypeDict = {
    type(None): SitoMinorType.NONE,
    type: SitoMinorType.TYPE,
    Callable: SitoMinorType.CALLABLE,
    bytes: SitoMinorType.BYTES,
    bool: SitoMinorType.PRIMITIVE,
    str: SitoMinorType.PRIMITIVE,
    int: SitoMinorType.PRIMITIVE,
    float: SitoMinorType.PRIMITIVE,
    complex: SitoMinorType.NUMBER,
    dict: SitoMinorType.MAPPING,
    list: SitoMinorType.SEQUENCE,
    tuple: SitoMinorType.SEQUENCE,
    set: SitoMinorType.SET,
    frozenset: SitoMinorType.SET
}
