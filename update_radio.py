import urllib.request
import json
import os

# 1. KBS API에서 최신 스트리밍 주소 가져오기
api_url = "https://cfpwwwapi.kbs.co.kr/api/v1/landing/live/channel_code/21"
req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        new_url = data['channel_item'][0]['service_url']
        print(f"Successfully fetched new URL: {new_url}")
except Exception as e:
    print(f"Error fetching API: {e}")
    exit(1)

channels_file = 'channels.txt'

# 2. channels.txt 파일이 없으면 새로 만들고, 있으면 기존 내용을 안전하게 수정
updated_lines = []
found = False

if os.path.exists(channels_file):
    with open(channels_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        if "KBS 1 라디오" in line:
            parts = line.split(',')
            channel_name = parts[0].strip()
            updated_lines.append(f"{channel_name},{new_url}\n")
            found = True
        else:
            updated_lines.append(line)

# 기존 파일에 "KBS 1라디오" 항목이 없거나 파일이 없었다면 새로 추가
if not found:
    updated_lines.append(f"KBS 1라디오,{new_url}\n")

try:
    with open(channels_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    print("channels.txt updated successfully!")
except Exception as e:
    print(f"Error writing channels.txt: {e}")
    exit(1)
