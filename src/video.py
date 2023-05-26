import json
import os

import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    def __init__(self, video_id: str):
        self.__apikey = os.getenv('YOUTUBE_DATA_API')
        self.video_id: str = video_id

        try:
            response = requests.get(f'https://www.youtube.com/{self.video_id}')
            if response.status_code == 404:
                raise HttpError
            # requests.get()

        except HttpError:
            self.video_title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

        else:
            self.__youtube = build('youtube', 'v3', developerKey=self.__apikey)
            self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video_id
                                                                 ).execute()
            self.video_title: str = self.__video_response['items'][0]['snippet']['title']  # название видео
            self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"  # ссылка на видео
            self.view_count: int = self.__video_response['items'][0]['statistics']['viewCount']  # количество просмотров
            self.like_count: int = self.__video_response['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self):
        return self.video_title

    def _printj(self) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self.__video_response, indent=2, ensure_ascii=False))

    # @property
    # def response(self):
    #     return self.__video_response


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}&list={self.playlist_id}'


if __name__ == '__main__':
    video1 = Video('dfvdg')
    # print(video1.response)

    # video1._printj()
    #
    # assert str(video1) == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'
    # assert video1.video_id == '9lO06Zxhu88'
    # assert video1.video_url == 'https://www.youtube.com/watch?v=9lO06Zxhu88'
    #
    # video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    # # video2._printj()
    #
    # assert str(video2) == 'Пушкин: наше все?'
    # assert video2.video_url == 'https://www.youtube.com/watch?v=BBotskuyw_M&list=PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'
