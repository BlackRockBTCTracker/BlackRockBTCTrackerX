"""
Test con datos inventados para ver cómo se vería el resumen semanal
"""
from weekly_history import get_weekly_summary
from pathlib import Path
import json

# Crear datos inventados de una semana completa
fake_history = [
    {"date": "Dec 11, 2025", "btc": 765000.0, "usd": 64000000000, "change": 2100.5},
    {"date": "Dec 12, 2025", "btc": 764200.0, "usd": 63850000000, "change": -800.0},
    {"date": "Dec 13, 2025", "btc": 767400.0, "usd": 64120000000, "change": 3200.0},
    {"date": "Dec 14, 2025", "btc": 768900.0, "usd": 64245000000, "change": 1500.0},
    {"date": "Dec 15, 2025", "btc": 768400.0, "usd": 64200000000, "change": -500.0},
    {"date": "Dec 16, 2025", "btc": 771200.0, "usd": 64435000000, "change": 2800.0},
    {"date": "Dec 17, 2025", "btc": 773547.0, "usd": 64630000000, "change": 2347.0},
]

# Guardar datos inventados
file_path = Path("weekly_data.json")
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(fake_history, f, indent=2)

print("="*60)
print("  VISTA PREVIA - RESUMEN SEMANAL")
print("  (con datos inventados)")
print("="*60)

# Obtener resumen
summary = get_weekly_summary()

if summary:
    print(f"\n📊 DATOS DEL RESUMEN:")
    print(f"   Período: {summary['start_date']} → {summary['end_date']}")
    print(f"   Días: {summary['days']}")
    print(f"   Holdings actuales: {summary['current_btc']:,.1f} BTC")
    print(f"   Cambio semanal: {summary['btc_change']:,.1f} BTC")
    print(f"   Días +: {summary['positive_days']}")
    print(f"   Días -: {summary['negative_days']}")
    
    # Generar el tweet exactamente como lo haría main.py
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
    
    btc_change_str = f"+{summary['btc_change']:,.1f}" if summary['btc_change'] >= 0 else f"{summary['btc_change']:,.1f}"
    current_btc = f"{summary['current_btc']:,.1f}"
    
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
    
    print("\n" + "="*60)
    print("  ASÍ SE VERÍA EL TWEET:")
    print("="*60)
    print()
    print(weekly_message)
    print()
    print("="*60)
    print("📝 [SIN IMAGEN - Solo texto]")
    print("="*60)

print("\n✅ Vista previa completada")
