"""
Script de prueba COMPLETO que simula todo el flujo sin publicar.
Muestra exactamente qué se publicaría en X.
"""

from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from history_storage import add_to_history, check_milestones, get_weekly_summary
from enhanced_tweet_generator import (
    generate_enhanced_daily_tweet,
    generate_milestone_tweet,
    generate_weekly_summary_tweet,
    should_post_weekly_summary
)
import os

def print_separator(title=""):
    """Imprime un separador visual."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'-'*70}\n")

def preview_tweet(title, message, has_image=False):
    """Muestra cómo se vería el tweet."""
    print_separator(title)
    print(message)
    if has_image:
        print("\n📷 [IMAGEN ADJUNTA]")
    print_separator()

def run_preview():
    """Ejecuta una vista previa completa del bot sin publicar."""
    
    print("\n" + "="*70)
    print("  🔍 VISTA PREVIA - SIMULACIÓN SIN PUBLICAR")
    print("  Muestra exactamente qué se publicaría en X")
    print("="*70)
    
    try:
        # 1. OBTENER DATOS
        print_separator("PASO 1: OBTENER DATOS")
        btc, usd, change, date = get_blackrock_data()
        print(f"✅ Datos obtenidos:\n")
        print(f"  🪙 BTC: {btc}")
        print(f"  💵 USD: {usd}")
        print(f"  ➕ Change: {change}")
        print(f"  📅 Date: {date}")
        
        # 2. ACTUALIZAR HISTORIAL
        print_separator("PASO 2: ACTUALIZAR HISTORIAL")
        add_to_history(btc, usd, change, date)
        print("✅ Historial actualizado")
        
        # 3. GENERAR IMAGEN (SOLO PREVIEW)
        print_separator("PASO 3: GENERAR IMAGEN")
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)
        print(f"✅ Imagen generada: {output_path}")
        
        # 4. TWEET DIARIO
        print_separator("PASO 4: TWEET DIARIO")
        daily_message = generate_enhanced_daily_tweet(btc, usd, change, date)
        preview_tweet("📱 TWEET DIARIO (Principal)", daily_message, has_image=True)
        
        # 5. VERIFICAR MILESTONES
        print_separator("PASO 5: VERIFICAR MILESTONES")
        milestones = check_milestones(btc, usd)
        
        if milestones:
            print(f"🎉 {len(milestones)} milestone(s) detectado(s)!\n")
            for i, milestone in enumerate(milestones, 1):
                milestone_message = generate_milestone_tweet(milestone)
                preview_tweet(f"📱 TWEET DE MILESTONE {i}/{len(milestones)}", 
                            milestone_message, has_image=True)
        else:
            print("ℹ️ No se detectaron nuevos milestones.")
            print("   Los milestones se detectan cuando se CRUZA el umbral.")
            print("   Umbrales: 700K, 750K, 800K BTC | $60B, $65B, $70B USD")
        
        # 6. VERIFICAR RESUMEN QUINCENAL
        print_separator("PASO 6: VERIFICAR RESUMEN QUINCENAL")
        
        if should_post_weekly_summary():
            print("✅ Es momento del resumen quincenal (1er o 3er domingo, 8-10 AM)\n")
            summary = get_weekly_summary()
            
            if summary:
                summary_message = generate_weekly_summary_tweet(summary)
                preview_tweet("📱 TWEET DE RESUMEN QUINCENAL", 
                            summary_message, has_image=True)
            else:
                print("⚠️ No hay suficientes datos para resumen (necesitas 2+ registros)")
        else:
            print("ℹ️ No es momento para resumen quincenal.")
            print("   Se publica automáticamente el 1er y 3er domingo del mes, 8-10 AM")
        
        # RESUMEN FINAL
        print_separator("📊 RESUMEN DE LA EJECUCIÓN")
        
        total_tweets = 1  # Diario siempre
        total_tweets += len(milestones) if milestones else 0
        total_tweets += 1 if (should_post_weekly_summary() and get_weekly_summary()) else 0
        
        print(f"Total de tweets que se publicarían: {total_tweets}")
        print(f"  • 1 tweet diario (siempre)")
        print(f"  • {len(milestones)} tweet(s) de milestone" if milestones else "  • 0 tweets de milestone")
        weekly_count = 1 if (should_post_weekly_summary() and get_weekly_summary()) else 0
        print(f"  • {weekly_count} tweet de resumen quincenal")
        
        print("\n💡 TIPS:")
        print("  • Los tweets se publican en orden: Diario → Milestones → Quincenal")
        print("  • Todos usan la misma imagen generada")
        print("  • El historial se guarda en btc_history.json")
        print("  • Milestones: 700K, 750K, 800K BTC | $60B, $65B, $70B | 3.5%, 4%, 4.5%")
        print("  • Resumen quincenal: 1er y 3er domingo del mes, 8-10 AM")
        
        print_separator("✅ VISTA PREVIA COMPLETADA")
        print("\n📝 PRÓXIMOS PASOS:")
        print("  1. Todo está listo! Solo haz commit y push")
        print("  2. GitHub Actions se encargará del resto automáticamente")
        print("  3. ¡Disfruta del engagement mejorado! 🚀\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_preview()
