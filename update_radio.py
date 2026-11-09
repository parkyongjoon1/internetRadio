import urllib.request
import json
import base64

# 1. KBS API에서 최신 KBS 1라디오(.m3u8) 스트리밍 주소 가져오기
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

# 2. 기존 channels.txt 파일을 읽어서 KBS 1라디오 주소만 싹 교체하기
# (channels.txt 파일 안에 KBS 1라디오 줄이 포함되어 있다고 가정합니다)
try:
    with open('channels.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    for line in lines:
        # KBS 1라디오 항목인 경우 주소를 최신 주소로 바꿔치기 합니다
        if "KBS 1 라디오" in line:
            # 예시 포맷: KBS 1라디오,http://최신주소
            # 저장하신 형식에 맞춰 이름과 주소를 콤마(,) 등으로 구분해 둡니다.
            parts = line.split(',')
            channel_name = parts[0]
            updated_lines.append(f"{channel_name},{new_url}\n")
        else:
            updated_lines.append(line)
            
    with open('channels.txt', 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    print("channels.txt updated successfully!")

except Exception as e:
    print(f"Error updating channels.txt: {e}")
    exit(1)
