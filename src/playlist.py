import datetime
import json
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        self.__api_key: str = os.getenv('YOUTUBE_DATA_API')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self._playlist_videos = self.__youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                    part='contentDetails,snippet',
                                                                    maxResults=50,
                                                                    ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self._playlist_videos['items']]
        self._video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                            id=','.join(video_ids)
                                                            ).execute()

        self.__channel_id = self._playlist_videos['items'][0]['snippet']['channelId']
        self._channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        playlists = self.__youtube.playlists().list(channelId=self.__channel_id,
                                                    part='contentDetails,snippet',
                                                    maxResults=50,
                                                    ).execute()
        # не понятно как сделать title по плейлист id! чтобы не указывать индекс вручную.
        self.title = playlists['items'][1]['snippet']['title']

        # for playlist in playlists['items']:
        # print(json.dumps(playlists, indent=2, ensure_ascii=False))
        # print()

    @property
    def total_duration(self):
        time_list = datetime.timedelta(0, 0, 0)
        for video in self._video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_list += duration

        return time_list

    def show_best_video(self):
        best_like = 0
        video_id = None
        for video in range(len(self._video_response) + 1):
            like_count = int(self._video_response['items'][video]['statistics']['likeCount'])

            if like_count > best_like:
                best_like = like_count
                video_id = self._video_response['items'][video]['id']

        return f'https://youtu.be/{video_id}'


if __name__ == '__main__':
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    # pl.total_duration()
    # print(json.dumps(pl._playlist_videos, indent=2, ensure_ascii=False))
    # print(json.dumps(pl._channel, indent=2, ensure_ascii=False))
    # print(json.dumps(pl._video_response, indent=2, ensure_ascii=False))
    # print(pl.total_duration())
    # print(str(pl.total_duration()))
    # print(type(pl.total_duration()))
    # print(pl.show_best_video())
