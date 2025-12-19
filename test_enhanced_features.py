"""
Script de prueba para las funcionalidades mejoradas.
No hace publicaciones reales, solo muestra cómo se verían los tweets.
"""

from scraper import get_blackrock_data
from history_storage import (
    add_to_history, 
    get_weekly_summary, 
    check_milestones,
    get_engagement_context,
    get_trend_analysis
)
from enhanced_tweet_generator import generate_all_tweets
import json

def print_separator(title=""):
    """Imprime un separador visual."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")

def test_data_scraping():
    """Prueba 1: Verificar que el scraper funciona."""
    print_separator("TEST 1: SCRAPING DE DATOS")
    
    try:
        btc, usd, change, date = get_blackrock_data()
        print(f"✅ Datos obtenidos exitosamente:\n")
        print(f"  🪙 BTC: {btc}")
        print(f"  💵 USD: {usd}")
        print(f"  ➕ Change: {change}")
        print(f"  📅 Date: {date}")
        return btc, usd, change, date
    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")
        return None

def test_history_storage(btc, usd, change, date):
    """Prueba 2: Verificar almacenamiento de historial."""
    print_separator("TEST 2: ALMACENAMIENTO DE HISTORIAL")
    
    try:
        entry = add_to_history(btc, usd, change, date)
        print(f"✅ Entrada agregada al historial:\n")
        print(json.dumps(entry, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error al guardar historial: {e}")

def test_engagement_context(change):
    """Prueba 3: Verificar generación de contexto de engagement."""
    print_separator("TEST 3: CONTEXTO DE ENGAGEMENT")
    
    try:
        context = get_engagement_context(change)
        print(f"✅ Contexto generado:\n")
        print(f"  Emoji: {context['emoji']}")
        print(f"  Tono: {context['tone']}")
        print(f"  Prefijo: {context['prefix']}")
        print(f"  Pregunta: {context['question']}")
    except Exception as e:
        print(f"❌ Error al generar contexto: {e}")

def test_milestones(btc, usd):
    """Prueba 4: Verificar detección de milestones."""
    print_separator("TEST 4: DETECCIÓN DE MILESTONES")
    
    try:
        milestones = check_milestones(btc, usd)
        if milestones:
            print(f"✅ {len(milestones)} Milestone(s) detectado(s):\n")
            for i, m in enumerate(milestones, 1):
                print(f"  {i}. {m['message']}")
        else:
            print("ℹ️ No se detectaron nuevos milestones (es normal si ya pasaron)")
    except Exception as e:
        print(f"❌ Error al detectar milestones: {e}")

def test_trend_analysis():
    """Prueba 5: Verificar análisis de tendencia."""
    print_separator("TEST 5: ANÁLISIS DE TENDENCIA")
    
    try:
        trend = get_trend_analysis()
        if trend:
            print(f"✅ Análisis generado:\n")
            print(f"  Tendencia: {trend['trend']}")
            print(f"  Días analizados: {trend['days_analyzed']}")
            print(f"  Días positivos: {trend['positive_days']}")
            print(f"  Días negativos: {trend['negative_days']}")
            print(f"  Cambio promedio: {trend['avg_change']:,.2f} BTC")
        else:
            print("ℹ️ No hay suficientes datos para análisis de tendencia")
            print("   (necesitas al menos 3 registros en el historial)")
    except Exception as e:
        print(f"❌ Error al analizar tendencia: {e}")

def test_weekly_summary():
    """Prueba 6: Verificar resumen semanal."""
    print_separator("TEST 6: RESUMEN SEMANAL")
    
    try:
        summary = get_weekly_summary()
        if summary:
            print(f"✅ Resumen generado:\n")
            print(f"  Período: {summary['start_date']} → {summary['end_date']}")
            print(f"  Días analizados: {summary['period_days']}")
            print(f"  Cambio BTC: {summary['btc_change']:,.2f}")
            print(f"  Cambio USD: ${summary['usd_change']:,.2f}")
            print(f"  Días positivos: {summary['positive_days']}")
            print(f"  Días negativos: {summary['negative_days']}")
            print(f"  Cambio diario promedio: {summary['avg_daily_change']:,.2f} BTC")
        else:
            print("ℹ️ No hay suficientes datos para resumen semanal")
            print("   (necesitas al menos 2 registros en el historial)")
    except Exception as e:
        print(f"❌ Error al generar resumen: {e}")

def test_tweet_generation(btc, usd, change, date):
    """Prueba 7: Verificar generación de tweets."""
    print_separator("TEST 7: GENERACIÓN DE TWEETS")
    
    try:
        tweets = generate_all_tweets(btc, usd, change, date)
        
        # Tweet diario
        if "daily" in tweets:
            print("✅ TWEET DIARIO GENERADO:")
            print_separator()
            print(tweets["daily"])
            print_separator()
        
        # Milestones
        if "milestones" in tweets:
            print(f"\n✅ {len(tweets['milestones'])} TWEET(S) DE MILESTONE:")
            for i, tweet in enumerate(tweets["milestones"], 1):
                print_separator(f"Milestone {i}")
                print(tweet)
                print_separator()
        
        # Resumen semanal
        if "weekly_summary" in tweets:
            print("\n✅ TWEET DE RESUMEN SEMANAL:")
            print_separator()
            print(tweets["weekly_summary"])
            print_separator()
        else:
            print("\nℹ️ No es momento para resumen semanal (se publica domingos 8-10 AM)")
            
    except Exception as e:
        print(f"❌ Error al generar tweets: {e}")
        import traceback
        traceback.print_exc()

def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*60)
    print("  🧪 PRUEBAS DE FUNCIONALIDADES MEJORADAS")
    print("  Sin publicaciones reales - Solo visualización")
    print("="*60)
    
    # Test 1: Scraping
    result = test_data_scraping()
    if not result:
        print("\n❌ No se pudieron obtener datos. Abortando pruebas.")
        return
    
    btc, usd, change, date = result
    
    # Test 2: Almacenamiento
    test_history_storage(btc, usd, change, date)
    
    # Test 3: Engagement
    test_engagement_context(change)
    
    # Test 4: Milestones
    test_milestones(btc, usd)
    
    # Test 5: Tendencia
    test_trend_analysis()
    
    # Test 6: Resumen semanal
    test_weekly_summary()
    
    # Test 7: Generación de tweets
    test_tweet_generation(btc, usd, change, date)
    
    print_separator("RESUMEN DE PRUEBAS")
    print("✅ Todas las pruebas completadas!")
    print("\n📝 Notas importantes:")
    print("  • Los milestones solo se detectan cuando se CRUZA el umbral")
    print("  • El resumen semanal solo se genera los domingos 8-10 AM")
    print("  • Necesitas varios registros históricos para ver todas las features")
    print("  • El archivo btc_history.json guarda hasta 90 días de datos")
    print("\n💡 Para simular múltiples días, ejecuta este script varias veces")
    print("   y edita manualmente btc_history.json con datos variados.")
    
if __name__ == "__main__":
    run_all_tests()
