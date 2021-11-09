from anteiapi.models.file import FileContent
from io import BytesIO
from os import path
from typing import Union
from requests import Session
from .endpoints import (
    ATTP,
    BASE_URL,
    REMOVEBG,
    TIKOK,
    TAFSIR_MIMPI,
    PHLOGO,
    TTP,
    TWIBON
)
from .tools import resp_checker, get_binary_from_string
from .models import (
    TafsirMimpi,
    Tiktok,
    File,
    DownloadUrl
)
__all__ = ['AnteiAPI']
class AnteiAPI(Session):
    """
    :param apikey: get your apikey [here]/[at] https://antei.codes 
    """
    def __init__(self, apikey:str) -> None:
        super().__init__()
        self.headers.update({'Authorization':apikey})
        self.apikey:str = apikey

    def TikTok(self, url:str)->Tiktok:
        """
        Tiktok Downloader (With/Without Watermark)

        :param url: str
        """
        return Tiktok(resp_checker(self.get(BASE_URL+TIKOK, params={'url':url})).json())

    def tafsir_mimpi(self, q:str)->TafsirMimpi:
        """
        :param q: str
        """
        return TafsirMimpi(resp_checker(self.get(BASE_URL+TAFSIR_MIMPI, params={'q':q})).json())

    def Twibbonizze(self, name:str, image:Union[BytesIO, str])->File:
        """
        Generate your Twibbon 

        :param name: twibbon name [https://www.twibbonize.com]
        :param image: Image Path / BytesIO Object
         """
        file:BytesIO = get_binary_from_string(image)
        return File(resp_checker(self.post(BASE_URL+TWIBON, params={'name':name}, files={'image':file})).json())

    def removebg(self, image:Union[BytesIO, str])->File:
        """
        Remove Background from image

        :param image: Image Path / BytesIO Object
        """
        file: BytesIO = get_binary_from_string(image)
        return File(resp_checker(self.post(BASE_URL+REMOVEBG, files={'image':file})).json())

    def phlogo(self, black: str, orange: str):
        """
        p*rnhub logo maker

        :param black: Black text
        :param orange: Orange Text 
        """
        return File(resp_checker(self.get(BASE_URL+PHLOGO, params={'x':black, 'y':orange})).json())

    def ttp(self, text: str):
        """
        text to image

        :param text: text
        """
        return FileContent(resp_checker(self.get(BASE_URL+TTP, params={'text': text})).content)
    
    def attp(self, text: str):
        """
        text to animated picture

        :param text: text
        """
        return FileContent(resp_checker(self.get(BASE_URL+ATTP)).content)

