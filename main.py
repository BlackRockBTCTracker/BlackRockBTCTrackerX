from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from tweet_uploader import post_to_twitter
import os
import sys

def run_blackrock_bot():
    try:
        # Obtener datos del scraper
        btc, usd, change, date = get_blackrock_data()
        print(f"[INFO] Valor actual BTC: {btc}, USD: {usd}")

        # Leer último valor guardado de la caché
        last_value = os.environ.get('LAST_DATE', '')
        print(f"[DEBUG] Última fecha en caché: {last_value}")
        print(f"[DEBUG] Fecha actual: {date}")

        # Verificar si la fecha es la misma que la última guardada
        if last_value == date:
            print("[INFO] No hay cambios en la fecha, no se genera imagen ni se publica tweet.")
            return
            
        if last_value:
            print(f"[INFO] Nueva fecha detectada: {date} (anterior: {last_value})")
        else:
            print("[INFO] Primera ejecución o no se encontró fecha anterior, se procederá a publicar.")

        # Crear directorio de imágenes si no existe
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generar imagen
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)

        # Formatear el cambio con + si no tiene signo negativo
        formatted_change = change if change.startswith('-') else f"+{change}"

        # Construir el mensaje del tweet
        message = (
            f"BlackRock Bitcoin ETF (IBIT) Update – {date}\n\n"
            f"🪙 Holdings: {btc} BTC\n"
            f"💵 USD Value: {usd}\n"
            f"➕ Change: {formatted_change} BTC\n\n"
            f"📊 Source: http://Bitbo.io\n\n"
            f"#Bitcoin #BlackRock #IBIT #BTCETF"
        )

        # Publicar el tweet con la imagen
        #post_to_twitter(message, output_path)

        # Guardar la fecha en el archivo de entorno para GitHub Actions
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'LAST_DATE={date}', file=fh)

        print("[SUCCESS] Imagen generada y tweet publicado exitosamente.")

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        # Asegurarse de que el script falle en caso de error
        sys.exit(1)

if __name__ == "__main__":
    run_blackrock_bot()
