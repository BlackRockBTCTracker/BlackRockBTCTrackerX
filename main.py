from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from tweet_uploader import post_to_twitter
from storage import read_last_value, write_last_value
from history_storage import add_to_history, check_milestones, get_weekly_summary
from enhanced_tweet_generator import (
    generate_enhanced_daily_tweet,
    generate_milestone_tweet,
    generate_weekly_summary_tweet,
    should_post_weekly_summary
)

import os

def run_blackrock_bot():
    try:
        # Obtener datos del scraper
        btc, usd, change, date = get_blackrock_data()
        print(f"🔍 Valor actual BTC: {btc}, USD: {usd}")

        # Leer último valor guardado (puede ser fecha o valor antiguo)
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

        # Agregar al historial
        print("📊 Guardando datos en historial...")
        add_to_history(btc, usd, change, date)

        # Crear directorio de imágenes si no existe
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generar imagen (solo para el tweet principal)
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)

        # ============================================
        # 1. TWEET DIARIO PRINCIPAL (CON ENGAGEMENT)
        # ============================================
        print("\n📝 Generando tweet diario mejorado...")
        daily_message = generate_enhanced_daily_tweet(btc, usd, change, date)
        
        print("📤 Publicando tweet diario...")
        post_to_twitter(daily_message, output_path)
        print("✅ Tweet diario publicado exitosamente.")

        # ============================================
        # 2. MILESTONES (SI SE ALCANZARON)
        # ============================================
        print("\n🎯 Verificando milestones...")
        milestones = check_milestones(btc, usd)
        
        if milestones:
            print(f"🎉 ¡{len(milestones)} milestone(s) detectado(s)!")
            for i, milestone in enumerate(milestones, 1):
                print(f"\n📝 Generando tweet de milestone {i}/{len(milestones)}...")
                milestone_message = generate_milestone_tweet(milestone)
                
                # Para milestones, usar la misma imagen
                print(f"📤 Publicando milestone {i}...")
                post_to_twitter(milestone_message, output_path)
                print(f"✅ Milestone {i} publicado exitosamente.")
        else:
            print("ℹ️ No se detectaron nuevos milestones.")

        # ============================================
        # 3. RESUMEN QUINCENAL (SI CORRESPONDE)
        # ============================================
        if should_post_weekly_summary():
            print("\n📊 Es momento del resumen quincenal...")
            summary = get_weekly_summary()
            
            if summary:
                print("📝 Generando tweet de resumen quincenal...")
                summary_message = generate_weekly_summary_tweet(summary)
                
                print("📤 Publicando resumen quincenal...")
                post_to_twitter(summary_message, output_path)
                print("✅ Resumen quincenal publicado exitosamente.")
            else:
                print("⚠️ No hay suficientes datos para resumen quincenal.")
        else:
            print("\nℹ️ No es momento para resumen quincenal (1er y 3er domingo del mes, 8-10 AM).")

        # Guardar la nueva fecha
        write_last_value(date)

        print("\n" + "="*60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_blackrock_bot()
