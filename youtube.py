import httplib2
import os
import sys

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"
#MISSING_CLIENT_SECRETS_MESSAGE = """

YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,message=MISSING_CLIENT_SECRETS_MESSAGE,scope=YOUTUBE_READONLY_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,http=credentials.authorize(httplib2.Http()))

# Retrieve the contentDetails part of the channel resource for the
# authenticated user's channel.
channels_response = youtube.channels().list(mine=True,part="contentDetails").execute()

for channel in channels_response["items"]:
    # From the API response, extract the playlist ID that identifies the list
    # of videos uploaded to the authenticated user's channel.
    uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        
    print "Videos in list %s" % uploads_list_id
            
    # Retrieve the list of videos uploaded to the authenticated user's channel.
    playlistitems_list_request = youtube.playlistItems().list(playlistId=uploads_list_id,part="snippet",maxResult=500)

while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()
    
    # Print information about each video.
    for playlist_item in playlistitems_list_response["items"]:
        title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        print "%s (%s)" % (title, video_id)
    playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request,playlistitems_list_response)