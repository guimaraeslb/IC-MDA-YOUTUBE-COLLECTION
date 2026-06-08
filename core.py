import requests
import pandas as pd
import get_videos_content
from dotenv import load_dotenv
import os
from datetime import datetime
from langdetect import detect

load_dotenv(override=True)

videos_info = []

def create_csv_file(videos_info):
    df = pd.DataFrame(videos_info)
    df.to_csv("dados.csv", index=False)

def get_formatted_date(original_date):
    date = datetime.fromisoformat(original_date.replace('Z', '+00:00'))
    date = date.strftime('%d-%m-%Y %H:%M:%S')

    return date

def add_post_to_video_list(video_info, query, collectedBy):
    video = {'video_title':'', 'post_description':'', 'post_published_at':'','video_channel_id': '', 'post_author_username':'', 'post_original_id': '', 'video_views_count': '', 'post_likes_count': '', 'post_shares_count': '', 'collectionDate': '', 'post_url': '', 'post_hashtags': '', 'post_validation_status': ''}
    video['video_title'] = video_info["snippet"]['title']  
    video['post_description'] = video_info["snippet"]['description']
    video['post_published_at'] = get_formatted_date(video_info["snippet"]['publishedAt'])
    video['video_channel_id'] = video_info["snippet"]['channelId']
    video['post_original_id'] = video_info["id"]['videoId']

    video_stats = get_videos_content.get_video_stats(video["post_original_id"])
    video_specific_infos = get_videos_content.get_video_specific_infos(video["post_original_id"])

    video['post_author_username'] = video_specific_infos["channelTitle"]
    video['video_views_count'] = video_stats["viewCount"]
    video['post_likes_count'] = video_stats["likeCount"]
    video['post_comments_count'] = video_stats["commentCount"]
    video['collectionDate'] = get_formatted_date(str(datetime.now()))
    video['post_url'] = "https://www.youtube.com/watch?v=" + video['post_original_id']
    video['post_hashtags'] = video_specific_infos["tags"]
    video['post_query'] = "termos: " + query if(collectedBy == "termos") else "perfis: " + video["post_author_username"]
    video['post_shares_count'] = ""
    video['post_validation_status'] = "VALID"
    videos_info.append(video)

def get_videos_by_terms():
    url = os.getenv("URL_SEARCH")
    search_terms = os.getenv("YOUTUBE_SEARCH_TERMS").split(',')

    try:
        for term in search_terms:
            params = {"key": os.getenv("YOUTUBE_API_KEY"), "part": "snippet", "order": "relevance", "publishedAfter": "2026-05-25T03:00:00.000Z", "publishedBefore": "2026-06-01T02:59:59.000Z", "q": term, "type": "video", "maxResults": 400, "relevanceLanguage": "pt", "regionCode": 'BR'}
            response = requests.get(url, params)
            data = (response.json()['items'])
        
            for video_info in data:
                try:
                    if(detect(video_info["snippet"]['title']) != "pt" or "&" in video_info["snippet"]['title']):
                        continue;
                except:
                    print("Erro ao detectar idioma do vídeo com título ", video_info["snippet"]["title"])
                else:
                    add_post_to_video_list(video_info, term, "termos")      
        print(len(videos_info), " vídeos foram coletados")
        create_csv_file(videos_info)
    except KeyError:
        print("O limite de requisições com a chave de API atual foi atingido. Atualize o valor de YOUTUBE_API_KEY no arquivo .env")

def get_videos_by_profiles():
    url = os.getenv("URL_SEARCH")
    channel_ids = os.getenv("YOUTUBE_CHANNEL_IDS").split(',')

    try:
        for channel_id in channel_ids:
            params = {"key": os.getenv("YOUTUBE_API_KEY"), "part": "snippet", "order": "relevance", "channelId": channel_id, "publishedAfter": "2026-05-25T03:00:00.000Z", "publishedBefore": "2026-06-01T02:59:59.000Z", "type": "video", "maxResults": 400, "relevanceLanguage": "pt", "regionCode": 'BR'}

            response = requests.get(url, params)
            data = (response.json()['items'])
        
            for video_info in data:
                try:
                    if(detect(video_info["snippet"]['title']) != "pt" or "&" in video_info["snippet"]['title']):
                        continue;
                except:
                    print("Erro ao detectar idioma do vídeo com título ", video_info["snippet"]["title"])
                else:
                    add_post_to_video_list(video_info, channel_id, "profiles")
        print(len(videos_info), " vídeos foram coletados")
        create_csv_file(videos_info)
    except KeyError:
        print("O limite de requisições com a chave de API atual foi atingido. Atualize o valor de YOUTUBE_API_KEY no arquivo .env")

def main():
    op = int(input("Tecle 1 para coleta por termos e 2 para coleta por perfis: "))

    if(op == 1): return get_videos_by_terms()
    elif (op == 2): return get_videos_by_profiles()
    else: print("Insira uma opção válida")

main()