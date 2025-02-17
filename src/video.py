import os
from googleapiclient.discovery import build


class Video:
    """
    Класс видео для ютуб-канала
    """
    api_key: str = os.getenv('YT_API_KEY')
    _youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализирует id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.playlists = None
        self.video_id = video_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls._youtube

    def get_info_from_playlists(self):
        """
        Получает информацию по видеоролику
        """
        if self.playlists is None:
            self.playlists = self.get_service().videos().list(part="snippet,statistics", id=self.video_id).execute()
        return self.playlists

    @property
    def title(self):
        """
        Возвращает название канала
        """
        self.get_info_from_playlists()
        try:
            return self.playlists['items'][0]['snippet']['title']
        except IndexError:
            return None

    @property
    def description(self):
        """
        Возвращает описание канала
        """
        self.get_info_from_playlists()
        try:
            return self.playlists['items'][0]['snippet']['description']
        except IndexError:
            return None

    @property
    def url(self):
        """
        Возвращает ссылку на канал
        """
        self.get_info_from_playlists()
        try:
            return f"https://www.youtube.com/watch?v={self.video_id}"
        except IndexError:
            return None

    @property
    def view_count(self):
        """
        Возвращает количество подписчиков
        """
        self.get_info_from_playlists()
        try:
            return int(self.playlists['items'][0]['statistics']['viewCount'])
        except IndexError:
            return None

    @property
    def like_count(self):
        """
        Возвращает количество видео
        """
        self.get_info_from_playlists()
        try:
            return self.playlists['items'][0]['statistics']['likeCount']
        except IndexError:
            return None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
