import os
import json
from googleapiclient.discovery import build


class Channel:
    """
    Класс для ютуб-канала
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализирует id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.number_videos = 0
        self.number_views = 0
    @property
    def channel_id(self):
        """
        Геттер __channel_id
        """
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def print_info(self) -> None:
        """
        Выводит словарь в json-подобном удобном формате с отступами
        """
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def playlists_info(self) -> None:
        '''
        Получаем данные по play-листам канала
        docs: https://developers.google.com/youtube/v3/docs/playlists/list
        '''

        playlists = self.youtube.playlists().list(channelId=self.__channel_id,
                                         part='contentDetails,snippet',
                                         maxResults=50,
                                         ).execute()
        for playlist in playlists['items']:
            self.number_videos += 1
            self.number_views += playlist["contentDetails"]["itemCount"]

    @property
    def title(self):
        """
        Возвращает название канала
        """
#        self.title = self.channel['items'][0]['snippet']['title']
        return self.channel['items'][0]['snippet']['title']

    @property
    def description(self):
        """
        Возвращает описание канала
        """
#       self.description =self.channel['items'][0]['snippet']['description']
        return self.channel['items'][0]['snippet']['description']

    @property
    def url(self):
        """
        Возвращает ссылку на канал
        """
#        self.url ="https://www.youtube.com/channel/" + self.channel['item'][0]['snippet']['id']
        return f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"

    @property
    def video_count(self):
        """
        Возвращает количество подписчиков
        """
#        self.subscriber_count =self.channel['item'][0]['statistics']['videoCount']
        return self.channel['items'][0]['statistics']['videoCount']

    def to_json(self, file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        Channel.playlists_info(self)
        data = {'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'video_count':self.video_count,
                'number_of_videos': self.number_videos,
                'number_views': self.number_views
                }
        with open(file_name, 'w',encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)
            print(json.dumps(data, indent=2, ensure_ascii=False))
