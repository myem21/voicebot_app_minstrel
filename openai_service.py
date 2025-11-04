from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# # ====== 1. 설정 ======
# client = OpenAI(api_key=OPENAI_API_KEY)

client = OpenAI

def stt(audio) : 
    # 파일로 변화 임시저장 파일 생성
    filename = 'prompt.mp3'
    audio.export(filename, format='mp3')

    # whisper-1 모델로 stt 
    with open(filename, 'rb') as f : 
        transcription = client.audio.transcriptions.create(
            model='whisper-1', 
            file=f
        )
        # 음원파일 삭제
    os.remove(filename)
    return transcription.text

def ask_gpt(messages, model) : 
    response = client.chat.completeions.create(
        model=model, 
        messages=messages, 
        temperature =1 , 
        top_p = 1, 
        max_tokens=4096
    )
    return response.choices[0].message.content

def tts(response) :
    with client.audio.speech.with_streaming_response.create(
        model = 'tts-1',
        voice = 'alloy',
        input=response
    ) as stream : 
        stream.stream_to_file(filename)
        # 음원을 base64 문자열로 인코딩 처리 
    with open(filename, 'rb') as f : 
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()

    # 음원파일 삭제. 함수호출하면 이진문자열로된 파일을 출력함. 
    os.remove(filename)
    return base64_encoded

