import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        apikey = os.getenv('YOUTUBE_DATA_API')
        youtube = build('youtube', 'v3', developerKey=apikey)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))


Channel('UCMCgOm8GZkHp8zJ6l7_hIuA').print_info()
