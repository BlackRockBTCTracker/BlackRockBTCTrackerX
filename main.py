from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from tweet_uploader import post_to_twitter
from storage import read_last_value, write_last_value

import os

def run_blackrock_bot():
    try:
        # Obtener datos del scraper
        btc, usd, change, date = get_blackrock_data()
        print(f"🔍 Valor actual BTC: {btc}, USD: {usd}")

        # Leer última fecha guardada
        last_date = read_last_value()
        print(f"🔍 Última fecha guardada: {last_date}")
        print(f"📅 Fecha actual: {date}")

        # Comparar con la última fecha
        if last_date == date:
            print("ℹ️ No hay cambios en la fecha, no se genera imagen ni se publica tweet.")
            return

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
        post_to_twitter(message, output_path)

        # Guardar la nueva fecha
        write_last_value(date)

        print("✅ Imagen generada y tweet publicado exitosamente.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_blackrock_bot()
