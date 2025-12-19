from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from tweet_uploader import post_to_twitter
from storage import read_last_value, write_last_value
from weekly_history import add_daily_data, get_weekly_summary, should_post_weekly

import os

def run_blackrock_bot():
    try:
        # Obtener datos del scraper
        btc, usd, change, date = get_blackrock_data()
        print(f"🔍 Valor actual BTC: {btc}, USD: {usd}")

        # Leer último valor guardado
        last_value = read_last_value()
        print(f"🔍 Último valor guardado: {last_value}")
        print(f"📅 Fecha actual: {date}")

        # Verificar si la fecha es la misma que la última guardada
        if last_value == date:
            print("ℹ️ No hay cambios en la fecha, no se genera imagen ni se publica tweet.")
            return
            
        if last_value:
            print(f"ℹ️ Nueva fecha detectada: {date} (anterior: {last_value})")
        else:
            print("ℹ️ Primera ejecución o no se encontró fecha anterior, se procederá a publicar.")

        # Guardar datos en historial semanal
        add_daily_data(btc, usd, change, date)

        # Crear directorio de imágenes si no existe
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generar imagen
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)

        # Formatear el cambio con + si no tiene signo negativo
        formatted_change = change if change.startswith('-') else f"+{change}"

        # Construir el mensaje del tweet diario
        message = (
            f"BlackRock Bitcoin ETF (IBIT) Update – {date}\n\n"
            f"🪙 Holdings: {btc} BTC\n"
            f"💵 USD Value: {usd}\n"
            f"➕ Change: {formatted_change} BTC\n\n"
            f"📊 Source: http://Bitbo.io\n\n"
            f"#Bitcoin #BlackRock #IBIT #BTCETF"
        )

        # Publicar el tweet diario
        post_to_twitter(message, output_path)
        print("✅ Tweet diario publicado exitosamente.")

        # Verificar si es domingo para resumen semanal
        if should_post_weekly():
            print("\n📊 Es domingo, verificando resumen semanal...")
            summary = get_weekly_summary()
            
            if summary:
                print("📝 Generando resumen semanal...")
                
                # Determinar magnitud del cambio
                change = summary["btc_change"]
                
                if change > 10000:
                    magnitude = "MASSIVE accumulation"
                    emoji = "🚀🚀"
                elif change > 5000:
                    magnitude = "Strong accumulation"
                    emoji = "🚀"
                elif change > 2000:
                    magnitude = "Solid accumulation"
                    emoji = "📈"
                elif change > 0:
                    magnitude = "Slight accumulation"
                    emoji = "➕"
                elif change > -2000:
                    magnitude = "Minor outflow"
                    emoji = "➖"
                elif change > -5000:
                    magnitude = "Notable outflow"
                    emoji = "📉"
                else:
                    magnitude = "HEAVY outflow"
                    emoji = "🔻🔻"
                
                # Formatear cambio semanal
                btc_change_str = f"+{summary['btc_change']:,.1f}" if summary['btc_change'] >= 0 else f"{summary['btc_change']:,.1f}"
                
                # Holdings actuales (último dato)
                current_btc = f"{summary['current_btc']:,.1f}"
                
                # Construir mensaje de resumen
                weekly_message = (
                    f"📊 WEEKLY SUMMARY\n\n"
                    f"📅 {summary['start_date']} → {summary['end_date']}\n\n"
                    f"🪙 Current Holdings: {current_btc} BTC\n"
                    f"📊 Weekly Change: {btc_change_str} BTC\n"
                    f"{emoji} {magnitude}\n\n"
                    f"📈 This Week:\n"
                    f"  ✅ Positive days: {summary['positive_days']}\n"
                    f"  ❌ Negative days: {summary['negative_days']}\n\n"
                    f"What's your prediction for next week? 💭\n\n"
                    f"#Bitcoin #BlackRock #IBIT #WeeklySummary"
                )
                
                # Publicar resumen semanal SIN imagen
                post_to_twitter(weekly_message, None)
                print("✅ Resumen semanal publicado exitosamente.")
            else:
                print("ℹ️ No hay suficientes datos para resumen semanal (necesitas al menos 2 días)")
        else:
            print("\nℹ️ No es domingo, no se publica resumen semanal.")

        # Guardar la nueva fecha
        write_last_value(date)

        print("\n✅ Proceso completado exitosamente.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_blackrock_bot()
