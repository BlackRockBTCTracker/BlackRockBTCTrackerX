"""
Script para simular diferentes escenarios con datos de ejemplo.
Muestra cómo se verían los tweets en diferentes situaciones.
"""

from enhanced_tweet_generator import (
    generate_enhanced_daily_tweet,
    generate_milestone_tweet,
    generate_weekly_summary_tweet
)
from history_storage import add_to_history, read_history, write_history
import json

def print_tweet(title, tweet):
    """Imprime un tweet con formato."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")
    print(tweet)
    print(f"\n{'='*70}\n")

def simulate_big_increase():
    """Simula un gran aumento de BTC."""
    print("\n🚀 ESCENARIO 1: GRAN AUMENTO (+5,000 BTC)")
    
    btc = "780,500.0"
    usd = "$68,500,000,000"
    change = "+5,342.8"
    date = "Dec 18, 2025"
    
    tweet = generate_enhanced_daily_tweet(btc, usd, change, date)
    print_tweet("Tweet Diario - Gran Aumento", tweet)

def simulate_moderate_increase():
    """Simula un aumento moderado."""
    print("\n📈 ESCENARIO 2: AUMENTO MODERADO (+2,500 BTC)")
    
    btc = "778,000.0"
    usd = "$67,800,000,000"
    change = "+2,405.2"
    date = "Dec 18, 2025"
    
    tweet = generate_enhanced_daily_tweet(btc, usd, change, date)
    print_tweet("Tweet Diario - Aumento Moderado", tweet)

def simulate_small_increase():
    """Simula un pequeño aumento."""
    print("\n➕ ESCENARIO 3: PEQUEÑO AUMENTO (+500 BTC)")
    
    btc = "776,000.0"
    usd = "$67,200,000,000"
    change = "+520.5"
    date = "Dec 18, 2025"
    
    tweet = generate_enhanced_daily_tweet(btc, usd, change, date)
    print_tweet("Tweet Diario - Pequeño Aumento", tweet)

def simulate_small_decrease():
    """Simula una pequeña disminución."""
    print("\n➖ ESCENARIO 4: PEQUEÑA DISMINUCIÓN (-1,000 BTC)")
    
    btc = "774,500.0"
    usd = "$66,800,000,000"
    change = "-1,142.0"
    date = "Dec 18, 2025"
    
    tweet = generate_enhanced_daily_tweet(btc, usd, change, date)
    print_tweet("Tweet Diario - Pequeña Disminución", tweet)

def simulate_big_decrease():
    """Simula una gran disminución."""
    print("\n📉 ESCENARIO 5: GRAN DISMINUCIÓN (-6,000 BTC)")
    
    btc = "770,000.0"
    usd = "$65,500,000,000"
    change = "-6,405.2"
    date = "Dec 18, 2025"
    
    tweet = generate_enhanced_daily_tweet(btc, usd, change, date)
    print_tweet("Tweet Diario - Gran Disminución", tweet)

def simulate_milestone_btc():
    """Simula alcanzar un milestone de BTC."""
    print("\n🎯 ESCENARIO 6: MILESTONE - 800K BTC")
    
    milestone_data = {
        "type": "btc",
        "value": 800000,
        "message": "🎉 BlackRock IBIT alcanzó 800,000 BTC!"
    }
    
    tweet = generate_milestone_tweet(milestone_data)
    print_tweet("Tweet de Milestone - BTC", tweet)

def simulate_milestone_usd():
    """Simula alcanzar un milestone de USD."""
    print("\n💰 ESCENARIO 7: MILESTONE - $70B USD")
    
    milestone_data = {
        "type": "usd",
        "value": 70000000000,
        "message": "💰 BlackRock IBIT superó $70B en valor!"
    }
    
    tweet = generate_milestone_tweet(milestone_data)
    print_tweet("Tweet de Milestone - USD", tweet)

def simulate_milestone_percentage():
    """Simula alcanzar un milestone de porcentaje."""
    print("\n📊 ESCENARIO 8: MILESTONE - 4% DEL SUPPLY")
    
    milestone_data = {
        "type": "percentage",
        "value": 4.0,
        "message": "📊 BlackRock IBIT ahora posee 4.0% de todo el Bitcoin!"
    }
    
    tweet = generate_milestone_tweet(milestone_data)
    print_tweet("Tweet de Milestone - Porcentaje", tweet)

def simulate_weekly_summary_positive():
    """Simula un resumen semanal positivo."""
    print("\n📊 ESCENARIO 9: RESUMEN SEMANAL - SEMANA POSITIVA")
    
    summary = {
        "period_days": 7,
        "start_date": "Dec 11, 2025",
        "end_date": "Dec 18, 2025",
        "start_btc": 765000.0,
        "end_btc": 775647.0,
        "btc_change": 10647.0,
        "usd_change": 892000000,
        "avg_daily_change": 1521.0,
        "positive_days": 5,
        "negative_days": 2,
        "total_changes": [2100, -800, 3200, 1500, -500, 2800, 2347]
    }
    
    tweet = generate_weekly_summary_tweet(summary)
    print_tweet("Resumen Semanal - Positivo", tweet)

def simulate_weekly_summary_negative():
    """Simula un resumen semanal negativo."""
    print("\n📊 ESCENARIO 10: RESUMEN SEMANAL - SEMANA NEGATIVA")
    
    summary = {
        "period_days": 7,
        "start_date": "Dec 11, 2025",
        "end_date": "Dec 18, 2025",
        "start_btc": 785000.0,
        "end_btc": 775647.0,
        "btc_change": -9353.0,
        "usd_change": -785000000,
        "avg_daily_change": -1336.1,
        "positive_days": 2,
        "negative_days": 5,
        "total_changes": [-2100, 800, -3200, -1500, 500, -2800, -1053]
    }
    
    tweet = generate_weekly_summary_tweet(summary)
    print_tweet("Resumen Semanal - Negativo", tweet)

def create_sample_history():
    """Crea un historial de ejemplo con 10 días de datos."""
    print("\n📝 BONUS: CREANDO HISTORIAL DE EJEMPLO")
    print("   Esto te permite probar el análisis de tendencias\n")
    
    sample_data = [
        {"date": "Dec 8, 2025", "btc": 765000.0, "usd": 64000000000, "change": 2100.0},
        {"date": "Dec 9, 2025", "btc": 764200.0, "usd": 63850000000, "change": -800.0},
        {"date": "Dec 10, 2025", "btc": 767400.0, "usd": 64120000000, "change": 3200.0},
        {"date": "Dec 11, 2025", "btc": 768900.0, "usd": 64245000000, "change": 1500.0},
        {"date": "Dec 12, 2025", "btc": 768400.0, "usd": 64200000000, "change": -500.0},
        {"date": "Dec 13, 2025", "btc": 771200.0, "usd": 64435000000, "change": 2800.0},
        {"date": "Dec 14, 2025", "btc": 773547.0, "usd": 64630000000, "change": 2347.0},
        {"date": "Dec 15, 2025", "btc": 774547.0, "usd": 64714000000, "change": 1000.0},
        {"date": "Dec 16, 2025", "btc": 778052.2, "usd": 65008000000, "change": 3505.2},
        {"date": "Dec 17, 2025", "btc": 775647.0, "usd": 64807000000, "change": -2405.2},
    ]
    
    # Agregar timestamp a cada entrada
    from datetime import datetime
    for entry in sample_data:
        entry["timestamp"] = datetime.now().isoformat()
    
    # Guardar el historial
    write_history(sample_data)
    
    print(f"✅ Historial de ejemplo creado con {len(sample_data)} días de datos")
    print(f"   Archivo: btc_history.json\n")
    print("   Ahora puedes ejecutar test_enhanced_features.py para ver:")
    print("   - Análisis de tendencias")
    print("   - Detección de patrones")
    print("   - Resumen semanal completo")

def run_all_simulations():
    """Ejecuta todas las simulaciones."""
    print("\n" + "="*70)
    print("  🎬 SIMULACIÓN DE ESCENARIOS")
    print("  Visualiza cómo se verían los tweets en diferentes situaciones")
    print("="*70)
    
    # Escenarios de tweets diarios
    simulate_big_increase()
    simulate_moderate_increase()
    simulate_small_increase()
    simulate_small_decrease()
    simulate_big_decrease()
    
    # Escenarios de milestones
    simulate_milestone_btc()
    simulate_milestone_usd()
    simulate_milestone_percentage()
    
    # Escenarios de resumen semanal
    simulate_weekly_summary_positive()
    simulate_weekly_summary_negative()
    
    # Crear historial de ejemplo
    print("\n" + "="*70)
    create_sample_history()
    
    print("\n" + "="*70)
    print("  ✅ SIMULACIONES COMPLETADAS")
    print("="*70)
    print("\n💡 PRÓXIMOS PASOS:")
    print("   1. Revisa cómo se ven los diferentes estilos de tweets")
    print("   2. Ejecuta: python test_enhanced_features.py")
    print("   3. Revisa el archivo btc_history.json generado")
    print("   4. Cuando estés listo, integra con main.py")
    print("\n")

if __name__ == "__main__":
    run_all_simulations()
