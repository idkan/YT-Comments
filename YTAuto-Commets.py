import sys
from random import sample

import googleapiclient
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from apiclient.errors import HttpError
from oauth2client.file import Storage

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Set DEVELOPER_KEY to the "API key" value from the Google Developers Console:
# https://console.developers.google.com/project/_/apiui/credential
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE ME"


def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes)

    credentials = flow.run_console()

    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def get_video_id(youtube_request):
    video_id = []
    next_page_token = None

    while True:
        video_id_request = youtube_request.search().list(
            part="id,snippet",
            order="date",
            channelId="UCqnFo90nZIcOxbfMekqnKiQ",
            maxResults=50,
            publishedAfter="2019-06-21T00:00:00.000Z",
            pageToken=next_page_token
        )
        response = video_id_request.execute()

        for i in response['items']:
            video_id.append(i['id']['videoId'])

        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    return video_id[:]


def like_video(youtube_request, id_video):
    for item in id_video:
        youtube_request.videos().rate(
            id=item,
            rating="like"
        ).execute()
        print(f'Liked video: {item}')


def comment_video(youtube_request, channel_id, id_video):
    comments = ['Buen video #JucaS3laSabe', 'Naves y Nenas por siempre #JucaS3laSabe',
                'Que naves!! #JucaS3laSabe', '#JucaS3laSabe Siempre presente en tus videos!!',
                '#JucaS3laSabe Presente!! como siempre', 'Siempre rifado con tus videos Juca! #JucaS3laSabe',
                '#JucaS3laSabe']
    for i in id_video:
        insert_result = youtube_request.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=channel_id,
                    videoId=i,
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=sample(comments, k=1))
                    )
                )
            )
        ).execute()

        comment = insert_result["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print(f'Inserted comment in Video id: {i} for: {author}: {text}')


if __name__ == "__main__":

    authenticated_service = get_authenticated_service()

    if DEVELOPER_KEY == "REPLACE ME":
        print("""You must set up a project and get an API key
                  to run this project. Please visit Google Developers
                  Page.""")
    else:
        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

        youtube_videoId_links = get_video_id(youtube)

        try:
            like_video(authenticated_service, youtube_videoId_links)
            comment_video(authenticated_service, 'UCqnFo90nZIcOxbfMekqnKiQ',
                          youtube_videoId_links)
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        else:
            print('Video has been liked.')
