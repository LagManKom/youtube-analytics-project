import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id

        self.__apikey = os.getenv('YOUTUBE_DATA_API')
        self.__youtube = build('youtube', 'v3', developerKey=self.__apikey)
        self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.__channel['items'][0]['snippet']['title']
        self.description = self.__channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel['items'][0]['id']}"
        self.subscriber_count = self.__channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.__channel['items'][0]['statistics']['videoCount']
        self.view_count = self.__channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print((json.dumps(self.__channel, indent=2, ensure_ascii=False)))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Получаем объект для работы с API"""
        apikey = os.getenv('YOUTUBE_DATA_API')
        youtube = build('youtube', 'v3', developerKey=apikey)
        return youtube

    def to_json(self, filename) -> None:
        """Создаём файл filename c данными по каналу"""
        with open(filename, 'w', encoding='utf-8') as file:
            data = {
                'id': self.__channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriberCount': self.subscriber_count,
                'videoCount': self.video_count,
                'viewCount': self.view_count
            }

            json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    channel = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    channel.print_info()
