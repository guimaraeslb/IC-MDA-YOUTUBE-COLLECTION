import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_video_stats(video_id):
    video_stats = {
        "viewCount": 0,
        "likeCount": 0,
        "commentCount": 0
    }

    params = {"key": os.getenv("YOUTUBE_API_KEY"), "part": "statistics", "id": video_id}
    response = requests.get(os.getenv('URL_VIDEOS'), params).json()

    if("viewCount" not in response["items"][0]["statistics"]):
        video_stats["viewCount"] = ""
    else:
        video_stats["viewCount"] = (response["items"][0]["statistics"]["viewCount"])
    
    if("likeCount" not in response["items"][0]["statistics"]):
        video_stats["likeCount"] = ""
    else:
        video_stats["likeCount"] = (response["items"][0]["statistics"]["likeCount"])

    if("commentCount" not in response["items"][0]["statistics"]):
        video_stats["commentCount"] = ""
    else:
        video_stats["commentCount"] = (response["items"][0]["statistics"]["commentCount"])
    return video_stats

def get_video_specific_infos(video_id):

    video_specific_infos = {
        "channelTitle": "",
        "tags": ""
    }
    params = {"key": os.getenv("YOUTUBE_API_KEY"), "part": "snippet", "id": video_id}
    response = requests.get(os.getenv('URL_VIDEOS'), params).json()

    video_specific_infos["channelTitle"] = (response["items"][0]["snippet"]["channelTitle"])

    if("tags" in response["items"][0]["snippet"]):
        video_specific_infos["tags"] = (response["items"][0]["snippet"]["tags"])
    else:
        video_specific_infos["tags"] = []
    return video_specific_infos