import requests


def ask_gemini(question, api_key, model="gemini-2.0-flash-001"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    response = requests.post(url, json={
        "contents": [{"parts": [{"text": question}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500}
    })

    if response.ok:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

API_KEY = "AIzaSyCtrFeQ16pW-WPzcUpp-N-IB1LwcmsaVlk"