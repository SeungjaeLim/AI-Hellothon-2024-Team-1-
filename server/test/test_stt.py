import requests

# Endpoint URL
url = "https://fjtskwttcrchrywg.tunnel-pt.elice.io/answers/"

# Open the converted audio file and send it as a file
with open("test_converted.wav", "rb") as audio_file:
    # Data payload with form fields and the file
    data = {
        "elder_id": 1,
        "question_id": 1
    }

    files = {
        "audio": ("test_converted.wav", audio_file, "audio/wav")  # Specify the correct MIME type for WAV
    }

    # Make the POST request
    response = requests.post(url, data=data, files=files)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())