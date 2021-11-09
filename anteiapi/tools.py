import requests
import re
import os
from typing import Union
from io import BytesIO
from .exception import (
    FileNotFound,
    ParameterInvalid,
    ParameterIsEmpty,
    AccessDenied,
    ApikeyNotValid,
    UrlNotValid,
    Limit
)
def get_binary_from_string(file:Union[BytesIO, str]):
    "file: path|url|BytesIO"
    if isinstance(file, BytesIO):
        return file
    elif os.path.isfile(file):
        return BytesIO(open(file, 'rb').read())
    elif re.match('https?://', file):
        return BytesIO(requests.get(file).content)
    raise FileNotFound(file.__str__())

def resp_checker(resp:requests.models.Response)->requests.models.Response:
    print(resp)
    if resp.status_code == 200:
        return resp
    err = {
        400:ParameterIsEmpty(resp.json().get('msg','')),
        402:Limit(resp.json().get('msg','')),
        403:AccessDenied(resp.json().get('msg','')),
        405:ApikeyNotValid(resp.json().get('msg','')),
        409:ParameterInvalid(resp.json().get('msg',''))
    }.get(resp.status_code)
    if err:
        raise err
    return resp
