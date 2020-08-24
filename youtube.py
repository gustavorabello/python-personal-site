import httplib2
import os
import sys

from apiclient.discovery import build
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
CLIENT_SECRETS_FILE = "client_secrets.json"

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

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READONLY_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

# Retrieve the contentDetails part of the channel resource for the
# authenticated user's channel.
channels_response = youtube.channels().list(
  mine=True,
  part="contentDetails"
).execute()

for channel in channels_response["items"]:
  # From the API response, extract the playlist ID that identifies the list
  # of videos uploaded to the authenticated user's channel.
  #uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
  uploads_list_id = "PLA5C4DB7CAE7AF003"

  print ("")
  print (" *************************************** ")
  print (" *  Videos in list %s" % uploads_list_id + "  * ")

  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_list_id,
    part="snippet",
    maxResults=50
  )

  count = 1
  while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    # print ("information about each video.")
    for playlist_item in playlistitems_list_response["items"]:
      title = playlist_item["snippet"]["title"]
      video_id = playlist_item["snippet"]["resourceId"]["videoId"]
      description = playlist_item["snippet"]["description"]
      date = playlist_item["snippet"]["publishedAt"][:10]+" "+\
             playlist_item["snippet"]["publishedAt"][11:19]
      videoid = "https://www.youtube.com/embed/"+\
                playlist_item["snippet"]["resourceId"]["videoId"]

      
      # grap video description using youtube.videos method.
      results = youtube.videos().list(
       part="contentDetails",
       id=video_id
       ).execute()
      print ("title: " + title)
      print ("video_id: " + video_id)
      #print ("description: " + description)
      duration = results["items"][0]["contentDetails"]["duration"][2:-1]

      savedir = "content/videos/" 

      file = open(savedir + str(count) + ".html",'w')
      file.write("---\n")
      file.write("title: " + title + "\n")
      file.write("duration: " + duration + "\n")
      file.write("created: !!timestamp '" + date + "'\n")
      file.write("tags: \n")
      file.write("    - two-phase \n")
      file.write("---\n")
      file.write("\n")
      file.write("{% mark video -%}\n")
      file.write("\n")
      file.write("<iframe src=\"" + videoid + "?rel=0" + "\"frameborder=\"1\" allowfullscreen></iframe> \n")
      file.write("\n")
      file.write("{% endmark %}\n")
      file.write("\n")
      file.write("\n")
      file.write("{% mark excerpt -%}\n")
      file.write(description[0:320])
      file.write("\n")
      file.write("{% endmark %}\n")
      file.write(description[320:])
      file.write("\n")
      file.close()
     
      count = count + 1
    
    playlistitems_list_request = youtube.playlistItems().list_next(
playlistitems_list_request, playlistitems_list_response)

  print (" *  Total number of videos: " + str(count-1) + "         * ")
  print (" *  Entries in the database ADDED:     * ")
  print (" *************************************** ")
  print ("")


