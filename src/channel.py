import os
import json
from googleapiclient.discovery import build


class Channel:
    """
    Класс для ютуб-канала
    """
    api_key: str = os.getenv('YT_API_KEY')
    _youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализирует id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.channel = None

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
        return cls._youtube

    def get_info_from_channel(self):
        """
        Получаем информацию о канале
        """
        if self.channel is None:
            self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return self.channel
    def print_info(self) -> None:
        """
        Выводит словарь в json-подобном удобном формате с отступами
        """
        self.get_info_from_channel()

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def title(self):
        """
        Возвращает название канала
        """
        self.get_info_from_channel()
        return self.channel['items'][0]['snippet']['title']

    @property
    def description(self):
        """
        Возвращает описание канала
        """
        self.get_info_from_channel()
        return self.channel['items'][0]['snippet']['description']

    @property
    def url(self):
        """
        Возвращает ссылку на канал
        """
        self.get_info_from_channel()
        return f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"

    @property
    def subscriber_count(self):
        """
        Возвращает количество подписчиков
        """
        self.get_info_from_channel()
        return int(self.channel['items'][0]['statistics']['subscriberCount'])

    @property
    def video_count(self):
        """
        Возвращает количество видео
        """
        self.get_info_from_channel()
        return self.channel['items'][0]['statistics']['videoCount']

    @property
    def view_count(self):
        """
        Возвращает количество просмотров видео
        """
        self.get_info_from_channel()
        return self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """
        метод __str__, возвращающий название и ссылку на канал
        по шаблону <название_канала> (<ссылка_на_канал>)
        """
        return f'{self.title}  {self.url}'

    def __add__(self, other):
        """
    	Метод сложения
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """
    	Метод вычитания
        """
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """
    	Метод для операции сравнения «больше»
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """
        Метод для операции сравнения «больше или равно»
        """
        return self.subscriber_count >= other.subscriber_count

    def __it__(self, other):
        """
        Метод для операции сравнения «меньше»
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """
        Метод для операции сравнения «меньше или равно»
        """
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """
        Метод определяет поведение оператора равенства, ==
        """
        return self.subscriber_count == other.subscriber_count

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
