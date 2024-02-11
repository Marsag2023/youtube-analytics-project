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
        return f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"

    @property
    def subscriber_count(self):
        """
        Возвращает количество подписчиков
        """
        return self.channel['items'][0]['statistics']['subscriberCount']

    @property
    def video_count(self):
        """
        Возвращает количество видео
        """
        return self.channel['items'][0]['statistics']['videoCount']

    @property
    def view_count(self):
        """
        Возвращает количество просмотров видео
        """
        return self.channel['items'][0]['statistics']['viewCount']

    def to_json(self, file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        data = {'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
                }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)
            print(json.dumps(data, indent=2, ensure_ascii=False))
