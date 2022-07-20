import requests
import os
import glob


#1.下載m3u8檔案
response=requests.get('https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/b6b8d175-68aa-31d8-bb0a-9ced8fdd70b6/2022-06-30/07-08-18/e3f21603-23b4-5a4a-bc9b-5d8b6e8362ca/stream_640x360x856_v2.m3u8')

if not os.path.exists('vedio'):
    os.mkdir('video')

with open ('video\\trailer.m3u8','wb') as file:
    file.write(response.content)

#2.下載ts檔案
ts_url_list=[]
with open('video\\trailer.m3u8','r', encoding='utf-8') as file:
    contents=file.readlines()
    base_url='https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/b6b8d175-68aa-31d8-bb0a-9ced8fdd70b6/2022-06-30/07-08-18/e3f21603-23b4-5a4a-bc9b-5d8b6e8362ca/'

    for content in contents:
        if content.endswith('ts\n'):
            ts_url=base_url+content.replace('\n','')
            ts_url_list.append(ts_url)

for index, url in enumerate(ts_url_list):
    ts_response=requests.get(url)

    with open(f'video\\{index+1}.ts', 'wb') as file:
        file.write(ts_response.content)

#3.合併ts檔案
ts_files=glob.glob('video\\*.ts')

with open('video\\trailer.mp4','wb') as file:
    for ts_file in ts_files:
        file.write(open(ts_file,'rb').read())
