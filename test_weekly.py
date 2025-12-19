"""
Test simple para el resumen semanal - NO PUBLICA NADA
"""
from scraper import get_blackrock_data
from weekly_history import add_daily_data, get_weekly_summary, should_post_weekly

print("="*60)
print("  TEST DE RESUMEN SEMANAL - SIN PUBLICAR")
print("="*60)

# 1. Obtener datos actuales
print("\n1. Obteniendo datos...")
btc, usd, change, date = get_blackrock_data()
print(f"✅ Datos: {btc} BTC, {usd}, Change: {change}")

# 2. Agregar al historial
print("\n2. Guardando en historial...")
add_daily_data(btc, usd, change, date)

# 3. Verificar si es domingo
print("\n3. Verificando día de la semana...")
is_sunday = should_post_weekly()
print(f"{'✅ Es domingo!' if is_sunday else 'ℹ️ No es domingo (resumen solo se publica domingos)'}")

# 4. Obtener resumen
print("\n4. Calculando resumen semanal...")
summary = get_weekly_summary()

if summary:
    print(f"\n✅ RESUMEN DISPONIBLE:")
    print(f"   Período: {summary['start_date']} → {summary['end_date']}")
    print(f"   Días analizados: {summary['days']}")
    print(f"   Cambio BTC: {summary['btc_change']:,.1f}")
    print(f"   Cambio USD: ${summary['usd_change']:,.0f}")
    print(f"   Días positivos: {summary['positive_days']}")
    print(f"   Días negativos: {summary['negative_days']}")
    
    # Mostrar cómo se vería el tweet
    btc_str = f"+{summary['btc_change']:,.1f}" if summary['btc_change'] >= 0 else f"{summary['btc_change']:,.1f}"
    usd_str = f"+${summary['usd_change']:,.0f}" if summary['usd_change'] >= 0 else f"-${abs(summary['usd_change']):,.0f}"
    total_days = summary['positive_days'] + summary['negative_days']
    success_rate = (summary['positive_days'] / total_days * 100) if total_days > 0 else 0
    
    if summary["btc_change"] > 5000:
        trend = "🚀 STRONG ACCUMULATION WEEK"
    elif summary["btc_change"] > 0:
        trend = "📈 Positive Week"
    elif summary["btc_change"] > -5000:
        trend = "📉 Slight Decrease"
    else:
        trend = "🔻 OUTFLOW WEEK"
    
    print("\n" + "="*60)
    print("  VISTA PREVIA DEL TWEET")
    print("="*60)
    
    weekly_message = (
        f"📊 WEEKLY SUMMARY\n"
        f"{trend}\n\n"
        f"📅 {summary['start_date']} → {summary['end_date']}\n\n"
        f"📊 Net Change:\n"
        f"  🪙 {btc_str} BTC\n"
        f"  💵 {usd_str}\n\n"
        f"📈 Performance:\n"
        f"  ✅ Positive days: {summary['positive_days']}\n"
        f"  ❌ Negative days: {summary['negative_days']}\n"
        f"  📊 Success rate: {success_rate:.0f}%\n\n"
        f"What's your prediction for next week? 💭\n\n"
        f"#Bitcoin #BlackRock #IBIT #WeeklySummary"
    )
    
    print(weekly_message)
    print("="*60)
else:
    print("\nℹ️ No hay suficientes datos aún (necesitas al menos 2 días)")
    print("   Ejecuta este script diariamente para acumular datos")

print("\n✅ Test completado - NO se publicó nada")
