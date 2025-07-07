import os
import requests
from requests_oauthlib import OAuth1

# Cargar las claves desde las variables de entorno (GitHub Actions las provee)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Endpoints de Twitter API v1.1
UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
POST_URL = "https://api.twitter.com/1.1/statuses/update.json"

# Autenticación OAuth1
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def post_to_twitter(tweet_text, image_path):
    # ---- Subir imagen ----
    with open(image_path, "rb") as image_file:
        response = requests.post(UPLOAD_URL, auth=auth, files={"media": image_file})
        if response.status_code != 200:
            raise Exception(f"❌ Error uploading image: {response.status_code} {response.text}")
        
        media_id = response.json().get("media_id_string")
        if not media_id:
            raise Exception(f"❌ Failed to retrieve media_id: {response.text}")
    
    print("✅ Imagen subida correctamente a Twitter.")

    # ---- Publicar Tweet ----
    payload = {
        "status": tweet_text,
        "media_ids": media_id
    }
    response = requests.post(POST_URL, auth=auth, params=payload)

    if response.status_code != 200:
        raise Exception(f"❌ Error posting tweet: {response.status_code} {response.text}")

    print("✅ Tweet publicado exitosamente.")