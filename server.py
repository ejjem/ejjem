from fastapi import FastAPI, File, UploadFile, HTTPException
from pydub import AudioSegment
import wave
import os
from datetime import datetime

# ffmpeg와 ffprobe 경로 설정
os.environ['FFMPEG_PATH'] = 'C:\\Program Files\\ffmpeg-7.0.1-essentials_build\\bin'
AudioSegment.ffmpeg = os.path.join(os.environ['FFMPEG_PATH'], 'ffmpeg.exe')
AudioSegment.ffprobe = os.path.join(os.environ['FFMPEG_PATH'], 'ffprobe.exe')

# 환경 변수 설정
os.environ['FFMPEG_PATH'] = 'C:/Program Files/ffmpeg-7.0.1-essentials_build/bin'

AudioSegment.ffmpeg = os.environ['FFMPEG_PATH'] + '/ffmpeg.exe'
AudioSegment.ffprobe = os.environ['FFMPEG_PATH'] + '/ffprobe.exe'

app = FastAPI()

# 파일을 저장할 디렉토리 설정
RAW_DIR = "raw"
WAV_DIR = "wav"
MP3_DIR = "mp3"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(WAV_DIR, exist_ok=True)
os.makedirs(MP3_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # 현재 시간으로 파일 이름 설정
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        raw_filename = os.path.join(RAW_DIR, f"{current_time}.raw")

        # 비트 데이터를 RAW 형식으로 저장
        with open(raw_filename, "wb") as f:
            f.write(contents)

        print(f"Saved RAW file: {raw_filename}")

        # RAW 파일을 WAV 파일로 변환
        wav_filename = raw_to_wav(raw_filename, current_time)

        print(f"Converted to WAV file: {wav_filename}")

        # WAV 파일을 MP3 파일로 변환
        mp3_filename = wav_to_mp3(wav_filename, current_time)

        print(f"Converted to MP3 file: {mp3_filename}")

        return {"raw_file": raw_filename, "wav_file": wav_filename, "mp3_file": mp3_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def raw_to_wav(raw_filename: str, current_time: str) -> str:
    try:
        wav_filename = os.path.join(WAV_DIR, f"{current_time}.wav")
        sample_rate = 44100  # 일반적으로 사용되는 샘플 레이트
        channels = 1  # 모노
        bit_depth = 16  # 16비트 오디오

        with open(raw_filename, "rb") as raw_file:
            raw_data = raw_file.read()

        wav_file = wave.open(wav_filename, 'w')
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(bit_depth // 8)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(raw_data)
        wav_file.close()

        return wav_filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting RAW to WAV: {str(e)}")

def wav_to_mp3(wav_filename: str, current_time: str) -> str:
    try:
        mp3_filename = os.path.join(MP3_DIR, f"{current_time}.mp3")
        audio = AudioSegment.from_wav(wav_filename)
        audio.export(mp3_filename, format="mp3")

        return mp3_filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting WAV to MP3: {str(e)}")
