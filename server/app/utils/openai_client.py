import openai
import os
from typing import List

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using OpenAI Whisper.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: The transcribed text.
    """
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return response["text"]


def summarize_text(content: str) -> str:
    """
    Summarize a given text using OpenAI GPT.
    Args:
        content (str): Text to summarize.
    Returns:
        str: Summarized text.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n{content}"}
        ]
    )
    return response["choices"][0]["message"]["content"]


def generate_title(content: str) -> str:
    """
    Generate a title for a given text using OpenAI GPT.
    Args:
        content (str): Text for which to generate a title.
    Returns:
        str: Generated title.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates titles."},
            {"role": "user", "content": f"Generate a title for the following content:\n{content}"}
        ]
    )
    return response["choices"][0]["message"]["content"]


def extract_keywords(content: str) -> List[str]:
    """
    Extract keywords from a given text using OpenAI GPT.
    Args:
        content (str): Text from which to extract keywords.
    Returns:
        List[str]: List of extracted keywords.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts keywords."},
            {"role": "user", "content": f"Extract keywords from the following text:\n{content}"}
        ]
    )
    keywords_text = response["choices"][0]["message"]["content"]
    return [keyword.strip() for keyword in keywords_text.split(",")]


def generate_image(prompt: str, size: str = "1024x1024") -> str:
    """
    Generate an image using OpenAI DALL-E.
    Args:
        prompt (str): Description of the image to generate.
        size (str): Image size (default: "1024x1024").
    Returns:
        str: URL of the generated image.
    """
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )
    return response["data"][0]["url"]
