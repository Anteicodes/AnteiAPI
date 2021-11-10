import requests
import re
import os
from typing import Union
from io import BytesIO

from requests.api import delete
from .exception import (
    FileNotFound,
    ParameterInvalid,
    ParameterIsEmpty,
    AccessDenied,
    ApikeyNotValid,
    UrlNotValid,
    Limit,
    IpError
)
def get_binary_from_string(file:Union[BytesIO, str]):
    """
    :param file: file path / BytesIO Object
    """
    if isinstance(file, BytesIO):
        return file
    elif os.path.isfile(file):
        return BytesIO(open(file, 'rb').read())
    elif re.match('https?://', file):
        return BytesIO(requests.get(file).content)
    raise FileNotFound(file.__str__())

def resp_checker(resp:requests.models.Response)->requests.models.Response:
    """
    :param resp: requests
    """
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

class IP:
    """
    :param IP: str
    :param session: Session Object
    """
    def __init__(self, IP, session) -> None:
        self.ip = IP
        self.session = session
    @property
    def delete(self):
        """
        delete ip from Ip Manager
        """
        js=self.session.post('https://antei.codes/api-ip', data={'AccessToken':self.session.access_token, 'action':'remove', 'ip':self.ip}).json()
        if not js['status']:
            raise IpError(js.get('msg','the problem is unknown'))
        return js['status']
    def __repr__(self) -> str:
        return f'<{self.ip}>'