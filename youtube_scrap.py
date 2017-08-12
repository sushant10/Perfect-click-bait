#Api key: AIzaSyApd_8osV3L1Ia212LbOTLyAn5dsZeLRNs
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pandas as pd 
import matplotlib.pyplot as plt

DEVELOPER_KEY = "AIzaSyApd_8osV3L1Ia212LbOTLyAn5dsZeLRNs" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#search term
argparser.add_argument("--q", help="Search term", default="gone wrong")
#max results
argparser.add_argument("--max-results", help="Max results", default=25)
args = argparser.parse_args()
options = args

#build service
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Call the search.list method to retrieve results matching the specified query term.
search_response = youtube.search().list(
 q=options.q,
 type="video",
 part="id,snippet",
 maxResults=options.max_results
).execute()

videos = {}

# Add each result to the appropriate list, and then display the lists of matching videos.
#Filter out channels, and playlists.
for search_result in search_response.get("items", []):
	if search_result["id"]["kind"] == "youtube#video":
 		#videos.append("%s" % (search_result["id"]["videoId"]))
 		videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

# print "Videos:\n", "\n".join(videos), "\n"

s = ','.join(videos.keys())
videos_list_response = youtube.videos().list(
 	id=s,
 	part='id,statistics'
).execute()
#videos_list_response['items'].sort(key=lambda x: int(x['statistics']['likeCount']), reverse=True)
#res = pd.read_json(json.dumps(videos_list_response['items']))
res = []
for i in videos_list_response['items']:
 	temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	temp_res.update(i['statistics'])
	res.append(temp_res)

df=pd.DataFrame.from_dict(res)


#down here is exxperiment
#testing graphs down here
"""fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Credit_History')
ax1.set_ylabel('Count of Applicants')
ax1.set_title("Applicants by Credit_History")
temp1.plot(kind='bar')

ax2 = fig.add_subplot(122)
temp2.plot(kind = 'bar')
ax2.set_xlabel('Credit_History')
ax2.set_ylabel('Probability of getting loan')
ax2.set_title("Probability of getting loan by credit history")"""
