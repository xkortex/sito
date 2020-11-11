from typing import Optional, List, Dict, Any

import numpy as np
import pandas as pd
import sklearn


class ArrayMeta(type):
    def __getitem__(self, t):
        return type("SitoArray", (SitoArray,), {"__dtype__": t})


class SitoArray(np.ndarray, metaclass=ArrayMeta):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        dtype = getattr(cls, "__dtype__", Any)
        if dtype is Any:
            return np.array(val)
        else:
            return np.array(val, dtype=dtype)

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(type="SitoArray")


class SitoEstimator(sklearn.base.BaseEstimator):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        assert isinstance(val, sklearn.base.BaseEstimator)
        return val

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="SitoEstimator")


class SitoDataFrame(pd.DataFrame):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        assert isinstance(val, pd.DataFrame)
        return val

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="SitoDataFrame")
