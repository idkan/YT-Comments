import json
from googleapiclient.discovery import build

# Set DEVELOPER_KEY to the "API key" value from the Google Developers Console:
# https://console.developers.google.com/project/_/apiui/credential
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = "REPLACE ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def main():
    if DEVELOPER_KEY == "REPLACE_ME":
        print("""You must set up a project and get an API key
                  to run this project. Please visit Google Developers
                  Page.""")
    else:

        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    video_id = []
    next_page_token = None

    while 1:
        video_id_request = youtube.search().list(
            part="id,snippet",
            order="date",
            channelId="UCqnFo90nZIcOxbfMekqnKiQ",
            maxResults=50,
            publishedAfter="2019-05-21T00:00:00.000Z",
            pageToken=next_page_token
        )
        response = video_id_request.execute()

        for i in response['items']:
            video_id.append((i['id']['videoId']))
        print(video_id)
        print(len(video_id))

        next_page_token = response['nextPageToken']

        if next_page_token is None:
            break


if __name__ == "__main__":
    main()
