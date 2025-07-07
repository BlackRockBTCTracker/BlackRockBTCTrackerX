import tweepy

# Cargar las claves desde las variables de entorno (GitHub Actions las provee)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def post_to_twitter(tweet_text, image_path):
    try:
        # Configurar la autenticación
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        
        # Configurar la API v1.1 para la subida de medios
        auth = tweepy.OAuth1UserHandler(
            API_KEY, 
            API_SECRET,
            ACCESS_TOKEN, 
            ACCESS_TOKEN_SECRET
        )
        api_v1 = tweepy.API(auth)
        
        # 1. Subir la imagen
        try:
            media = api_v1.media_upload(image_path)
            print("✅ Imagen subida correctamente a Twitter.")
            
            # 2. Publicar el tweet con la imagen
            response = client.create_tweet(
                text=tweet_text,
                media_ids=[media.media_id]
            )
            
            print("✅ Tweet publicado exitosamente.")
            return response.data
            
        except tweepy.TweepyException as e:
            raise Exception(f"❌ Error de la API de Twitter: {str(e)}")
        
    except Exception as e:
        print(f"❌ Error en post_to_twitter: {str(e)}")
        raise
