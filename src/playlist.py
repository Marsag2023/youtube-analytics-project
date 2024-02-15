import datetime
import isodate
from src.channel import Channel


class PlayList(Channel):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    @property
    def playlist_videos(self):
        """
        Получаем данные по видеороликам в плейлисте
        """
        return self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                        part='contentDetails',
                                                        maxResults=50,
                                                        ).execute()

    @property
    def video_ids(self):
        """
        Получаем  id видео из плейлиста
        """

        return [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

    @property
    def video_response(self):
        """
        Выводим видеоролики из плейлиста с длительностью
        """
        return self.get_service().videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)).execute()

    @property
    def title(self):
        """
        Определяем название видео
        """
        return self.get_service().playlists().list(id=self.playlist_id, part='snippet').execute()["items"][0]["snippet"]["title"]

    @property
    def url(self):
        """
        Определяем ссылку на видео
        """
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        """
        Выводим длительность видеоролика из плейлиста
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """
        Ищем видео с наибольшим количеством лайков и возвращаем url видео
        """
        max_like = 0
        id_video = None
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])

            if like_count > max_like:
                max_like = like_count
                id_video = video['id']
        return f'https://youtu.be/{id_video}'
