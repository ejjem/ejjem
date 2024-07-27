import requests

# 서버 주소와 엔드포인트 설정
url = "http://127.0.0.1:8080/upload/"

# 비트 데이터 예제
bit_data = bytearray([0x00, 0x01, 0x02, 0x03, 0x04])

# 파일 형식으로 데이터를 보내기 위해 바이너리 파일로 저장
with open("test.raw", "wb") as f:
    f.write(bit_data)

# 파일 전송
with open("test.raw", "rb") as f:
    files = {"file": ("test.raw", f, "application/octet-stream")}
    response = requests.post(url, files=files)

# 서버의 응답 상태 코드 및 내용 출력
print("Status Code:", response.status_code)
print("Response Content:", response.text)

# JSON 응답이 있을 경우 출력
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response")
