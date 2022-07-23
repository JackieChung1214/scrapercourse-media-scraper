import requests
import os
import glob


#1.下載m3u8檔案
response=requests.get('https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/61877050-d583-312d-bf21-e17b77107a57/2022-07-18/03-00-13/94027a58-9cf3-537d-9286-c54c64ed0c34/stream_640x360x440_v2.m3u8')

if not os.path.exists('vedio'):
    os.mkdir('video')

with open ('video\\trailer.m3u8','wb') as file:
    file.write(response.content)

#2.下載ts檔案
ts_url_list=[]
with open('video\\trailer.m3u8','r', encoding='utf-8') as file:
    contents=file.readlines()
    base_url='https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/61877050-d583-312d-bf21-e17b77107a57/2022-07-18/03-00-13/94027a58-9cf3-537d-9286-c54c64ed0c34/'

    for content in contents:
        if content.endswith('ts\n'):
            ts_url=base_url+content.replace('\n','')
            ts_url_list.append(ts_url)

for index, url in enumerate(ts_url_list):
    ts_response=requests.get(url)

    with open(f'video\\{index+1}.ts', 'wb') as file:
        file.write(ts_response.content)

#3.合併ts檔案
ts_files = sorted(glob.glob('video\\*.ts'), key=os.path.getmtime)

with open('video\\trailer.mp4','wb') as file:
    for ts_file in ts_files:
        file.write(open(ts_file,'rb').read())
