from openai import OpenAI
client = OpenAI()

import os
from typing import List
import requests
from uuid import uuid4

# Load OpenAI API key from environment variables
client.api_key = os.getenv("OPENAI_API_KEY")


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
