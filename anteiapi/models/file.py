from datetime import datetime
import requests
from filetype import guess_mime, guess_extension
from ..exception import FileNotFound
from io import BytesIO
class FileContent:
    """
    :param binary: bytes 
    """
    def __init__(self, binary: bytes) -> None:
        self.binary = binary
        self.mime: str = guess_mime(self.binary) or 'text/txt'
        self.extension: str = guess_extension(self.binary) or 'txt'
    def save(self, filename=False):
        """ save file

        :param filename: str
        """
        if isinstance(filename, str):
            open(filename, 'wb').write(self.binary)
        else:
            return BytesIO(self.binary)
class DownloadUrl:
    """
    :param url: str
    """
    def __init__(self, url) -> None:
        self.url = url
        self.req = requests.get(url, stream=True)
        if not self.req.status_code == 200:
            raise FileNotFound('')
        self.size = self.req.headers.get('Length-Content','Unknown')
        self.mime = self.req.headers.get('Content-Type','/')
        self.ext  = self.mime.split('/')[1]
        #expiration is not available
    def download(self)->BytesIO:
        """
        Download File from url
        """
        return BytesIO(requests.get(self.url).content)
    def __repr__(self) -> str:
        return """
{
    url: "%s",
    size: %s,
    mime: %s,
    ext: %s
    download: %s
}"""%(self.url, self.size, self.mime, self.download)
    def __str__(self) -> str:
        return self.__repr__()

class File:
    """
    :param jsun: dict
    """
    def __init__(self, jsun:dict) -> None:
        self.filename:str        = jsun['filename']
        self.mime:str            = jsun['mime']
        self.ext:str             = jsun['ext']
        self.expiration:datetime = datetime.fromtimestamp(jsun['expired'])
        self.filesize:int        = jsun['filesize']
        self.filesize_s:str      = jsun['filesize_s']
        self.url:str             = jsun['url']
    def download(self) -> BytesIO:
        """
        Download File from url
        """
        return BytesIO(requests.get(self.url).content)
    def __repr__(self) -> str:
        return f'<({self.filename})>'