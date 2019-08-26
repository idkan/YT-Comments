import os
import sys

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

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

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Set DEVELOPER_KEY to the "API key" value from the Google Developers Console:
# https://console.developers.google.com/project/_/apiui/credential
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCB3AQSOr4wOpEN50uGNUl01VjUx4CqOmg"


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_READ_WRITE_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


def get_video_id(youtube_request):
    video_id = []
    next_page_token = None

    while True:
        video_id_request = youtube_request.search().list(
            part="id,snippet",
            order="date",
            channelId="UCqnFo90nZIcOxbfMekqnKiQ",
            maxResults=50,
            publishedAfter="2019-05-21T00:00:00.000Z",
            pageToken=next_page_token
        )
        response = video_id_request.execute()

        for i in response['items']:
            video_id.append(i['id']['videoId'])

        next_page_token = response['nextPageToken']

        if next_page_token is None:
            break

    return video_id[:]


def like_video(youtube_request, id_video):

    for i in id_video:
        youtube_request.videos().rate(
            id=i,
            rating="like"
        ).execute()


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
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        else:
            print('Video has been liked.')