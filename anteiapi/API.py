import json
import requests
from html import unescape
from functools import namedtuple
from bs4 import BeautifulSoup
from anteiapi.models.file import FileContent
from io import BytesIO
import re
from typing import NamedTuple, Union
from requests import Session
from .endpoints import (
    ATTP,
    REMOVEBG,
    TIKOK,
    TAFSIR_MIMPI,
    PHLOGO,
    TTP,
    TWIBON
)
from .exception import EmailPasswordAreWrong, IpError, AccountError
from .tools import resp_checker, get_binary_from_string, IP
from .models import (
    TafsirMimpi,
    Tiktok,
    File,
)
__all__ = ['AnteiAPI', 'Login']
class AnteiAPI(Session):
    """
    :param apikey: get your apikey [here]/[at] https://antei.codes 
    """
    BASE_URL = 'https://antei.codes/'
    def __init__(self, apikey:str) -> None:
        super().__init__()
        self.headers.update({'Authorization':apikey})
        self.apikey:str = apikey

    def TikTok(self, url:str)->Tiktok:
        """
        Tiktok Downloader (With/Without Watermark)

        :param url: str
        """
        return Tiktok(resp_checker(self.get(self.BASE_URL+TIKOK, params={'url':url})).json())

    def tafsir_mimpi(self, q:str)->TafsirMimpi:
        """
        :param q: str
        """
        return TafsirMimpi(resp_checker(self.get(self.BASE_URL+TAFSIR_MIMPI, params={'q':q})).json())

    def Twibbonizze(self, name:str, image:Union[BytesIO, str])->File:
        """
        Generate your Twibbon 

        :param name: twibbon name [https://www.twibbonize.com]
        :param image: Image Path / BytesIO Object
         """
        file:BytesIO = get_binary_from_string(image)
        return File(resp_checker(self.post(self.BASE_URL+TWIBON, params={'name':name}, files={'image':file})).json())

    def removebg(self, image:Union[BytesIO, str])->File:
        """
        Remove Background from image

        :param image: Image Path / BytesIO Object
        """
        file: BytesIO = get_binary_from_string(image)
        return File(resp_checker(self.post(self.BASE_URL+REMOVEBG, files={'image':file})).json())

    def phlogo(self, black: str, orange: str):
        """
        p*rnhub logo maker

        :param black: Black text
        :param orange: Orange Text 
        """
        return File(resp_checker(self.get(self.BASE_URL+PHLOGO, params={'x':black, 'y':orange})).json())

    def ttp(self, text: str):
        """
        text to image

        :param text: text
        """
        return FileContent(resp_checker(self.get(self.BASE_URL+TTP, params={'text': text})).content)
    
    def attp(self, text: str):
        """
        text to animated picture

        :param text: text
        """
        return FileContent(resp_checker(self.get(self.BASE_URL+ATTP)).content)
    def __repr__(self) -> str:
        return f'<({self.apikey[:7]}...)>'

class Login(requests.Session):
    """
    :param num_email: phone_number | email
    :param password: password
    """
    __all__ = ['AnteiAPI', 'ip', 'add_ip', 'get_info', 'reset_apikey','logout']
    def __init__(self, num_email, password, **kwargs) -> None:
        super().__init__(**kwargs)
        resp = self.get('https://antei.codes/login')
        self.middleware = re.findall(r'name=\"csrfmiddlewaretoken\".*?value=\"(.*?)\"', resp.text)[0]
        result = self.post('https://antei.codes/login', data={'csrfmiddlewaretoken':self.middleware, 'email':num_email,'password':password})
        bs = BeautifulSoup(result.text, 'html.parser')
        self.name = bs.find_all('div', attrs={'class':'profile-detail mt-3'})[0].h3.text
        self.type = bs.find_all('div', attrs={'class':'profile-detail mt-3'})[0].span.text
        if "icon: 'error'," in result.text and bs.title != 'Home':
            raise EmailPasswordAreWrong()
        self.apikey = bs.find_all('input', attrs={'id':'key'})[0]['value']
        dashboard = self.get('https://antei.codes/dashboard').text
        self.access_token =  re.findall(r'AccessToken \= \"(.*?)\"', dashboard)[0]
    
    @property
    def AnteiAPI(self):
        """
        API
        """
        return AnteiAPI(self.apikey)

    def __enter__(self):
        return self
    
    def __exit__(self, *args) -> None:
        self.logout()
    
    @property
    def ip(self):
        """
        get list of allowed ip
        """
        return [IP(x, self) for x in json.loads(unescape(re.findall(r'htmlDecode\(\"(.*?)\"\)',self.get('https://antei.codes/dashboard').text)[0]))]

    def add_ip(self, ip: str)-> bool:
        """
        :param ip: str
        """
        status = self.post('https://antei.codes/api-ip', data={'AccessToken':self.access_token, 'action':'add', 'ip':ip}).json()
        if not status['status']:
            raise IpError(status.get('msg','the problem is unknown'))
        return status['status']
    
    @property
    def get_info(self)->NamedTuple:
        """
        Get Account Infomation
        """
        return namedtuple('API', ['name', 'apikey', 'requests', 'max_requests', 'max_ip', 'access_token'])(*re.findall(r'nama = \"(.*?)\"\n.*?apikey\=\"(.*?)\"\n.*?hit=([0-9]+)\n.*?max_hit = ([0-9]+)\n.*?max_ip = ([0-9]+)\n.*?\n.*?AccessToken \= \"(.*?)\"', self.get('https://antei.codes/dashboard').text)[0])
    
    @property
    def reset_apikey(self):
        """
        Reset Your Apikey
        """
        api=self.post('https://antei.codes/api-reset', data={'AccessToken':self.access_token}).json().get('apikey')
        if api:
            self.apikey=api
        return api
    
    def logout(self):
        """
        Logout 
        """
        if self.get('https://antei.codes/logout').status_code == 200:
            return True
        else:
            raise AccountError('your account already logout')
    
    def __repr__(self):
        return f'<[name: "{self.name}" type: "{self.type}"]>'