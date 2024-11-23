import requests

# Endpoint URL for re_answer
url = "https://fjtskwttcrchrywg.tunnel-pt.elice.io/answers/re_answer/2"

# Open the converted audio file and send it as a file
with open("test_converted.wav", "rb") as audio_file:
    # File payload
    files = {
        "audio": ("test_converted.wav", audio_file, "audio/wav")  # Specify the correct MIME type for WAV
    }

    # Make the POST request
    response = requests.post(url, files=files)

# Print the response
print("Status Code:", response.status_code)
try:
    print("Response Body:", response.json())
except ValueError:
    print("Response is not JSON:", response.text)
