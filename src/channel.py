import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id

        apikey = os.getenv('YOUTUBE_DATA_API')
        youtube = build('youtube', 'v3', developerKey=apikey)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/channel/{channel['items'][0]['id']}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        apikey = os.getenv('YOUTUBE_DATA_API')
        youtube = build('youtube', 'v3', developerKey=apikey)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        print((json.dumps(channel, indent=2, ensure_ascii=False)))

    @classmethod
    def get_service(cls):
        """Получаем объект для работы с API"""
        apikey = os.getenv('YOUTUBE_DATA_API')
        youtube = build('youtube', 'v3', developerKey=apikey)
        return youtube

    def to_json(self, filename) -> None:
        """Создаём файл filename c данными по каналу"""
        with open(filename, 'w', encoding='utf-8') as file:
            apikey = os.getenv('YOUTUBE_DATA_API')
            youtube = build('youtube', 'v3', developerKey=apikey)
            channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
            json.dump(channel, file, indent=4)


if __name__ == '__main__':
    Channel('UCMCgOm8GZkHp8zJ6l7_hIuA').print_info()
