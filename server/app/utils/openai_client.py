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
    Summarize a given text using OpenAI GPT.
    Args:
        content (str): Text to summarize.
    Returns:
        str: Summarized text.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n{content}"}
        ]
    )
    print("Summarized text: ", response.choices[0].message.content)
    return response.choices[0].message.content


def generate_title(content: str) -> str:
    """
    Generate a title for a given text using OpenAI GPT.
    Args:
        content (str): Text for which to generate a title.
    Returns:
        str: Generated title.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates titles."},
            {"role": "user", "content": f"Generate a title for the following content:\n{content}"}
        ]
    )
    print("Title: ", response.choices[0].message.content)
    return response.choices[0].message.content


def extract_keywords(content: str) -> List[str]:
    """
    Extract keywords from a given text using OpenAI GPT.
    Args:
        content (str): Text from which to extract keywords.
    Returns:
        List[str]: List of extracted keywords.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts keywords. just keyword and comma separated"},
            {"role": "user", "content": f"Extract keywords from the following text:\n{content}"}
        ]
    )
    keywords_text = response.choices[0].message.content
    print("Keywords: ", keywords_text)
    return [keyword.strip() for keyword in keywords_text.split(",")]

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
    Generate a follow-up question using OpenAI GPT.
    Args:
        question_answer_pairs (List[dict]): List of question-answer pairs.
    Returns:
        str: Generated follow-up question.
    """
    context = "\n".join(
        [f"Q: {pair['question']}\nA: {pair['answer']}" for pair in question_answer_pairs]
    )
    prompt = (
        "Based on the following conversation history, generate a meaningful follow-up question:"
        f"\n\n{context}\n\nFollow-up question:"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates follow-up questions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_text_embedding(text: str) -> List[float]:
    """
    Get the embedding for a given text using OpenAI's embedding model.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
