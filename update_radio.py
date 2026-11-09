import urllib.request
import json
import os

# 띄어쓰기가 반영된 채널 이름과 KBS API 채널 코드 설정
channels_to_update = {
    "KBS 1 라디오": "21",
    "KBS 클래식 FM": "24",
    "KBS 해피 FM": "22"
}

# 1. 각 채널별로 최신 스트리밍 주소 가져오기
fetched_channels = {}
for name, code in channels_to_update.items():
    api_url = f"https://cfpwwwapi.kbs.co.kr/api/v1/landing/live/channel_code/{code}"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            new_url = data['channel_item'][0]['service_url']
            fetched_channels[name] = new_url
            print(f"Successfully fetched {name}: {new_url}")
    except Exception as e:
        print(f"Error fetching API for {name}: {e}")
        exit(1)

channels_file = 'channels.txt'

# 2. channels.txt 파일 읽기 및 띄어쓰기 반영 업데이트
updated_lines = []
existing_channels = set()

if os.path.exists(channels_file):
    with open(channels_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        matched = False
        for name, new_url in fetched_channels.items():
            # 공백 유무와 관계없이 기존 라디오 채널명을 정확히 찾아 매칭
            if name.replace(" ", "") in line.replace(" ", ""):
                updated_lines.append(f"{name},{new_url}\n")
                existing_channels.add(name)
                matched = True
                break
        if not matched:
            updated_lines.append(line)

# 파일에 아직 없었던 채널이라면 아래에 새로 추가
for name, new_url in fetched_channels.items():
    if name not in existing_channels:
        updated_lines.append(f"{name},{new_url}\n")

# 3. 파일에 최종 저장하기
try:
    with open(channels_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    print("channels.txt updated successfully with proper spacing!")
except Exception as e:
    print(f"Error writing channels.txt: {e}")
    exit(1)
