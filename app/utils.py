from time import time 
from uuid import uuid4
from typing import Union

__all__ = ("get_time", "get_uuid")

def get_time(seconds_precision=True) -> Union[int, float]:
    return time() if not seconds_precision else int(time())

def get_uuid() -> str:
    return str(uuid4())