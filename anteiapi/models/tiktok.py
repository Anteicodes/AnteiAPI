import __future__
from .file import DownloadUrl

class MusicTiktok:
    """
    :param jsun: dict
    """
    def __init__(self, jsun: dict) -> None:
        self.thumbnail:DownloadUrl = DownloadUrl(jsun['thumbnail'])
        self.title: str = jsun['title']
        self.url: DownloadUrl = DownloadUrl(jsun['url'])
    def __repr__(self) -> str:
        return self.title

class VideoTiktok:
    """
    :param jsun: dict
    """
    def __init__(self, jsun) -> None:
        self.thumbnail: DownloadUrl = DownloadUrl(jsun['thumbnail'])
        self.duration: int = jsun['duration']
        self.wm: DownloadUrl = DownloadUrl(jsun['url_wm'])
        self.no_wm: DownloadUrl = DownloadUrl(jsun['url_nowm'])
    def __repr__(self) -> str:
        return f'<(Duration: {self.duration})>'

class Author:
    def __init__(self, name, id, username, avatar, verified):
        self.name: str = name
        self.id: str = id
        self.username: str = username
        self.avatar: DownloadUrl = DownloadUrl(avatar)
        self.verified: str = verified
    def __repr__(self) -> str:
        return f'<(@{self.username})>'

class Tiktok:
    """
    :param jsun: dict
    """
    def __init__(self, jsun:dict) -> None:
        self.description:str = jsun['description']
        self.jsun = jsun
        self.likes:str = jsun['likes']
        self.comments:str = jsun['comments']
        self.shares: str = jsun['shares']
        self.plays: str = jsun['plays']
    
    @property
    def author(self)->Author:
        return Author(**self.jsun['author'])

    @property
    def music(self)->MusicTiktok:
        return MusicTiktok(self.jsun['music'])

    @property
    def video(self):
        return MusicTiktok(self.jsun['music'])

    def __repr__(self) -> str:
        return f'<(@{self.author})>'


