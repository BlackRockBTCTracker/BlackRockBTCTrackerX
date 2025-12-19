import tweepy

# Credenciales de la API de Twitter (OAuth 1.0a)
API_KEY = "fAtUAee6ERA07Yi4thoRKRmle"
API_SECRET = "X96zLhhEoH5a5dilOOqAk1TjWBwB14qGNBiRz49jwJThNv2oTp"
ACCESS_TOKEN = "1940561534935040001-AIJuV5SaMZKytQB2g2blXciBuS3E4T"
ACCESS_TOKEN_SECRET = "HuwKuloMtNujiOpZjue76kvZkYUdp9CSyiBKiW77cIKbs"

def post_to_twitter(tweet_text, image_path):
    try:
        # Configurar la autenticación
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        
        # Si hay imagen, subirla primero
        media_id = None
        if image_path:
            # Configurar la API v1.1 para la subida de medios
            auth = tweepy.OAuth1UserHandler(
                API_KEY, 
                API_SECRET,
                ACCESS_TOKEN, 
                ACCESS_TOKEN_SECRET
            )
            api_v1 = tweepy.API(auth)
            
            try:
                media = api_v1.media_upload(image_path)
                media_id = media.media_id
                print("✅ Imagen subida correctamente a Twitter.")
            except tweepy.TweepyException as e:
                raise Exception(f"❌ Error al subir imagen: {str(e)}")
        
        # Publicar el tweet (con o sin imagen)
        try:
            if media_id:
                response = client.create_tweet(
                    text=tweet_text,
                    media_ids=[media_id]
                )
            else:
                response = client.create_tweet(text=tweet_text)
            
            print("✅ Tweet publicado exitosamente.")
            return response.data
            
        except tweepy.TweepyException as e:
            raise Exception(f"❌ Error de la API de Twitter: {str(e)}")
        
    except Exception as e:
        print(f"❌ Error en post_to_twitter: {str(e)}")
        raise
