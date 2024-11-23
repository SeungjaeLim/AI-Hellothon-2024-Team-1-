from openai import OpenAI
client = OpenAI()

import os
from typing import List
import requests
from uuid import uuid4
import base64
from pathlib import Path
# Load OpenAI API key from environment variables
client.api_key = os.getenv("OPENAI_API_KEY")
ELICE_API_URL = os.getenv("ELICE_API_URL")
ELICE_API_TOKEN = os.getenv("ELICE_API_TOKEN")
ELICE_TTS_API_URL = os.getenv("ELICE_TTS_API_URL")

def generate_tts_openai(text: str, save_dir: str = "./static/tts/", file_name: str = "openai_tts.mp3") -> str:
    """
    Generate speech from text using OpenAI's TTS API.

    Args:
        text (str): Text to synthesize into speech.
        save_dir (str): Directory to save the generated TTS audio (default: "./static/tts/").
        file_name (str): Name of the output TTS audio file (default: "openai_tts.mp3").

    Returns:
        str: Path to the saved TTS audio file.
    """
    # Ensure the save directory exists
    save_dir_path = Path(save_dir)
    save_dir_path.mkdir(parents=True, exist_ok=True)

    # Define the path for the generated TTS file
    speech_file_path = save_dir_path / file_name

    # Call OpenAI's TTS API
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )

    # Stream the generated audio to the specified file path
    response.stream_to_file(speech_file_path)

    return str(speech_file_path)

def generate_tts(text: str, audio_path: str = "./app/reference_audio.mp3", save_dir: str = "./static/tts/") -> str:
    """
    Generate speech from text using the Elice TTS API.

    Args:
        audio_path (str): Path to the reference audio file.
        text (str): Text to synthesize into speech.
        save_dir (str): Directory to save the generated TTS audio (default: "./static/tts/").

    Returns:
        str: Relative path to the saved TTS audio file.
    """
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Prepare files and payload for the API request
    files = {
        "audio": (os.path.basename(audio_path), open(audio_path, "rb"), "audio/mpeg")
    }
    payload = {
        "text": text
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ELICE_API_TOKEN}"
    }

    # Send the request to the Elice API
    response = requests.post(ELICE_TTS_API_URL, files=files, data=payload, headers=headers)

    # Check for a successful response
    if response.status_code != 200:
        raise Exception(f"TTS generation failed with status code {response.status_code}: {response.text}")

    # Decode and save the TTS audio file
    tts_audio_data = response.content
    file_name = os.path.basename(audio_path).replace(".mp3", "_tts.mp3")
    local_file_path = os.path.join(save_dir, file_name)

    with open(local_file_path, "wb") as file:
        file.write(tts_audio_data)

    # Return the relative path for API response
    return f"{save_dir}/{file_name}"

def generate_image_elice(prompt: str, style: str = "oil_painting", width: int = 256, height: int = 256, steps: int = 4, num: int = 1, save_dir: str = "./static/images/") -> str:
    """
    Generate an image using the Elice AI Hellothon API and save it locally.
    
    Args:
        prompt (str): Description of the image to generate.
        style (str): Style of the image (default: "polaroid").
        width (int): Width of the generated image (default: 256).
        height (int): Height of the generated image (default: 256).
        steps (int): Number of diffusion steps (default: 1).
        num (int): Number of images to generate (default: 1).
        save_dir (str): Directory to save the image (default: "./static/images/").
    
    Returns:
        str: Relative path to the saved image.
    """
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # API request payload
    payload = {
        "prompt": prompt,
        "style": style,
        "width": width,
        "height": height,
        "steps": steps,
        "num": num
    }
    
    headers = {
        "Authorization": f"Bearer {ELICE_API_TOKEN}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    # Send the request to the Elice API
    response = requests.post(ELICE_API_URL, headers=headers, json=payload)
    
    # Check for a successful response
    if response.status_code != 200:
        raise Exception(f"Image generation failed with status code {response.status_code}: {response.text}")
    
    # Decode the Base64 image
    image_data = response.json().get("predictions")
    if not image_data:
        raise Exception("No image data received from the API.")
    
    # Save the image locally
    file_name = f"{uuid4()}.png"
    local_file_path = os.path.join(save_dir, file_name)
    with open(local_file_path, "wb") as file:
        file.write(base64.b64decode(image_data))
    
    # Return the relative path for the API response
    return f"/static/images/{file_name}"

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using OpenAI Whisper.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: The transcribed text.
    """
    with open(file_path, "rb") as audio_file:
        print(audio_file)
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        print(response)
    return response.text


def summarize_text(content: str) -> str:
    """
    질의와 응답을 바탕으로 꼬리 질문이 이어진 노인의 일기 형식으로 텍스트를 재구성합니다.

    Args:
        content (str): 질의-응답 형식의 원문 텍스트.
    
    Returns:
        str: 노인의 일기 형식으로 변환된 텍스트.
    """
    example = """
    예시:
    질의와 응답:
    Q: 오늘 기분은 어떠셨나요?
    A: 괜찮았어요. 아침에 딸이랑 산책 다녀왔거든요.
    Q: 산책하면서 특별히 기억에 남는 게 있었나요?
    A: 길가에 코스모스가 너무 예쁘게 피었더라고요. 딸이 사진도 찍어줬어요.
    Q: 꽃을 보니 어떤 생각이 드셨나요?
    A: 어릴 때 아빠랑 코스모스 밭에 갔던 기억이 났어요. 그때도 이런 향기였죠.

    결과 (일기 형식):
    오늘은 참 기분 좋은 하루였어요. 아침에 딸이랑 함께 산책을 다녀왔거든요. 길가에 코스모스가 활짝 피어 있어서 발걸음을 멈추고 한참 바라봤답니다. 딸이 제 사진도 찍어줬는데, 꽃과 함께 찍은 제 모습이 마음에 들더라고요.

    꽃 향기를 맡으니 어릴 적 아빠랑 코스모스 밭을 거닐던 기억이 떠올랐어요. 그때도 지금처럼 이런 향기가 가득했는데, 그 시절의 따뜻함이 느껴지는 하루였답니다.
    """
    prompt = f"""
    다음 질의와 응답을 참고하여 자연스럽고 따뜻한 문체로 하루 일기를 작성하세요. 
    각 응답을 하나로 엮어 이야기를 구성하고, 노인의 경험과 감정이 담길 수 있도록 세부적으로 작성하세요.
    답변은 한 줄로 구성하며, 줄바꿈 없이 깔끔하게 작성하세요.
    특수문자(\\, \", \')는 결과에 포함되지 않도록 주의하세요.

    {example}

    질의와 응답:
    {content}

    결과 (일기 형식):
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 노인들의 이야기를 일기 형식으로 재구성하는 따뜻한 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def generate_title(content: str) -> str:
    """
    주어진 텍스트 내용을 바탕으로 적절한 제목을 생성합니다.
    Args:
        content (str): 제목을 생성할 텍스트.
    Returns:
        str: 생성된 제목.
    """
    example = """
    예시:
    텍스트 내용:
    "오늘 아침에는 아들과 함께 된장찌개를 먹으며 여행 계획을 세웠습니다. 봄에 제주도를 가기로 했고, 한라산에 오르고 싶다는 이야기를 나눴습니다."

    생성된 제목:
    "봄날의 제주도 여행과 가족의 따뜻한 식사"
    """
    prompt = f"""
    다음 텍스트를 읽고, 내용을 잘 요약하며 독자의 관심을 끌 수 있는 매력적인 제목을 생성하세요. 제목은 간결하면서도 내용을 잘 반영해야 합니다. 답변은 한 줄로 구성하며, 줄바꿈 없이 깔끔하게 작성하세요. 특수문자(\\, \", \')는 결과에 포함되지 않도록 주의하세요.

    {example}

    텍스트 내용:
    {content}

    생성된 제목:
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 주어진 텍스트에 적합한 제목을 만드는 능숙한 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()



def extract_keywords(content: str) -> List[str]:
    """
    주어진 텍스트에서 최대 5개의 핵심 키워드를 추출합니다.
    Args:
        content (str): 키워드를 추출할 텍스트.
    Returns:
        List[str]: 추출된 키워드 리스트 (최대 5개).
    """
    example = """
    예시:
    텍스트 내용:
    "봄날 가족과 함께 떠나는 제주도 여행 계획. 한라산 등반과 전통 시장 방문."
    
    생성된 키워드:
    제주도, 가족, 한라산, 여행, 전통 시장
    """
    prompt = f"""
    아래 텍스트를 읽고, 가장 중요한 키워드 최대 5개를 쉼표로 구분하여 추출하세요.
    키워드는 명확하고 간결하게 작성해야 하며, 중복되거나 관련 없는 단어는 피하세요.


    {example}

    텍스트 내용:
    {content}

    생성된 키워드:
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 주어진 텍스트에서 중요한 키워드를 추출하는 능숙한 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    # 결과를 쉼표로 구분된 키워드로 반환
    keywords_text = response.choices[0].message.content.strip()
    print("Keywords: ", keywords_text)
    return [keyword.strip() for keyword in keywords_text.split(",")][:5]  # 최대 5개의 키워드만 반환


def generate_image(prompt: str, size: str = "1024x1024", save_dir: str = "./static/images/") -> str:
    """
    Generate an image using OpenAI DALL-E and save it locally.
    
    Args:
        prompt (str): Description of the image to generate.
        size (str): Image size (default: "1024x1024").
        save_dir (str): Directory to save the image (default: "./static/images/").
        
    Returns:
        str: Relative path to the saved image.
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )
    
    # Get the image URL
    image_url = response.data[0].url
    
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Create a unique file name
    file_name = f"{uuid4()}.png"
    local_file_path = os.path.join(save_dir, file_name)
    
    # Download and save the image locally
    response = requests.get(image_url)
    with open(local_file_path, "wb") as file:
        file.write(response.content)
    
    # Return the relative path for API response
    return f"/static/images/{file_name}"


def generate_follow_up_question(question_answer_pairs: List[dict]) -> str:
    """
    Generate a follow-up question with empathy and continuity using OpenAI GPT.
    Args:
        question_answer_pairs (List[dict]): List of question-answer pairs.
    Returns:
        str: Empathetic response and a follow-up question.
    """
    example = """
    예시:
    대화 내역:
    Q: 오늘 특별히 기억에 남는 일이 있었나요?
    A: 아침에 마을회관에서 친구들과 윷놀이를 했어요. 정말 재밌었어요.
    Q: 어떤 점이 가장 즐거우셨나요?
    A: 친구들과 옛날 이야기도 하면서 웃고 떠들었던 게 정말 즐거웠어요.

    공감과 꼬리 질문:
    아, 친구들과 함께 윷놀이를 하셨군요! 옛날 이야기를 하면서 웃고 떠드는 시간이 정말 즐거웠을 것 같아요. 
    그럼 다음엔 친구들과 함께 어떤 활동을 하고 싶으신가요?
    """
    context = "\n".join(
        [f"Q: {pair['question']}\nA: {pair['answer']}" for pair in question_answer_pairs]
    )
    prompt = f"""
    아래의 대화 내역을 참고하여, 먼저 응답에 공감과 칭찬을 담은 문장을 작성한 후 자연스럽고 관련 있는 꼬리 질문을 만들어 주세요.
    노인의 감정과 경험을 존중하며, 긍정적인 분위기를 유지하도록 노력하세요.
    답변은 한 줄로 구성하며, 줄바꿈 없이 깔끔하게 작성하세요.
    특수문자(\\, \", \')는 결과에 포함되지 않도록 주의하세요.

    {example}

    대화 내역:
    {context}

    공감과 꼬리 질문:
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 노인들과의 대화를 이어가는 따뜻하고 공감 능력이 뛰어난 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def get_text_embedding(text: str) -> List[float]:
    """
    Get the embedding for a given text using OpenAI's embedding model.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
