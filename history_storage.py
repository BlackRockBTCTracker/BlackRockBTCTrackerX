import json
from pathlib import Path
from datetime import datetime, timedelta

HISTORY_FILE = "btc_history.json"

def read_history():
    """
    Lee el historial completo de datos de BTC.
    
    Returns:
        list: Lista de diccionarios con datos históricos
    """
    try:
        file_path = Path(HISTORY_FILE)
        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Error al leer historial: {e}")
    return []

def write_history(history_data):
    """
    Guarda el historial completo de datos.
    
    Args:
        history_data: Lista de diccionarios con datos históricos
    """
    try:
        file_path = Path(HISTORY_FILE)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Historial actualizado: {len(history_data)} registros")
    except Exception as e:
        print(f"❌ Error al guardar historial: {e}")
        raise

def add_to_history(btc, usd, change, date):
    """
    Añade un nuevo registro al historial.
    
    Args:
        btc: Holdings en BTC
        usd: Valor en USD
        change: Cambio en BTC
        date: Fecha del registro
    """
    history = read_history()
    
    # Parsear valores numéricos
    btc_float = float(btc.replace(",", ""))
    usd_float = float(usd.replace("$", "").replace(",", ""))
    change_float = float(change.replace(",", ""))
    
    new_entry = {
        "date": date,
        "btc": btc_float,
        "usd": usd_float,
        "change": change_float,
        "timestamp": datetime.now().isoformat()
    }
    
    # Verificar si ya existe este registro (por fecha)
    existing = [h for h in history if h.get("date") == date]
    if existing:
        print(f"ℹ️ Ya existe registro para {date}, actualizando...")
        history = [h for h in history if h.get("date") != date]
    
    history.append(new_entry)
    
    # Mantener solo últimos 90 días para no ocupar mucho espacio
    if len(history) > 90:
        history = history[-90:]
    
    write_history(history)
    return new_entry

def get_weekly_summary():
    """
    Calcula el resumen de la última semana.
    
    Returns:
        dict: Estadísticas de la semana o None si no hay suficientes datos
    """
    history = read_history()
    if len(history) < 2:
        return None
    
    # Últimos 7 registros (aproximadamente una semana)
    weekly_data = history[-7:] if len(history) >= 7 else history
    
    first = weekly_data[0]
    last = weekly_data[-1]
    
    btc_change = last["btc"] - first["btc"]
    usd_change = last["usd"] - first["usd"]
    
    # Calcular promedio de cambios diarios
    daily_changes = [entry["change"] for entry in weekly_data]
    avg_daily_change = sum(daily_changes) / len(daily_changes)
    
    # Días positivos vs negativos
    positive_days = len([c for c in daily_changes if c > 0])
    negative_days = len([c for c in daily_changes if c < 0])
    
    return {
        "period_days": len(weekly_data),
        "start_date": first["date"],
        "end_date": last["date"],
        "start_btc": first["btc"],
        "end_btc": last["btc"],
        "btc_change": btc_change,
        "usd_change": usd_change,
        "avg_daily_change": avg_daily_change,
        "positive_days": positive_days,
        "negative_days": negative_days,
        "total_changes": daily_changes
    }

def check_milestones(btc, usd):
    """
    Verifica si se alcanzaron nuevos hitos importantes.
    
    Args:
        btc: Holdings actuales en BTC (string con formato)
        usd: Valor actual en USD (string con formato)
        
    Returns:
        list: Lista de milestones alcanzados
    """
    milestones = []
    
    # Parsear valores
    btc_float = float(btc.replace(",", ""))
    usd_float = float(usd.replace("$", "").replace(",", ""))
    
    history = read_history()
    if not history:
        return milestones
    
    last_entry = history[-1]
    
    # Milestones de BTC (cada 10k)
    btc_milestones = [700000, 750000, 800000, 850000, 900000, 950000, 1000000]
    for milestone in btc_milestones:
        if last_entry["btc"] < milestone <= btc_float:
            milestones.append({
                "type": "btc",
                "value": milestone,
                "message": f"🎉 BlackRock IBIT alcanzó {milestone:,} BTC!"
            })
    
    # Milestones de USD (cada $5B)
    usd_milestones_b = [60, 65, 70, 75, 80, 85, 90, 95, 100]  # en billones
    for milestone_b in usd_milestones_b:
        milestone = milestone_b * 1_000_000_000
        if last_entry["usd"] < milestone <= usd_float:
            milestones.append({
                "type": "usd",
                "value": milestone,
                "message": f"💰 BlackRock IBIT superó ${milestone_b}B en valor!"
            })
    
    # % del supply total de Bitcoin
    total_btc = 21_000_000
    percentage = (btc_float / total_btc) * 100
    last_percentage = (last_entry["btc"] / total_btc) * 100
    
    # Milestones de % (cada 0.5%)
    percentage_milestones = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    for milestone_pct in percentage_milestones:
        if last_percentage < milestone_pct <= percentage:
            milestones.append({
                "type": "percentage",
                "value": milestone_pct,
                "message": f"📊 BlackRock IBIT ahora posee {milestone_pct}% de todo el Bitcoin!"
            })
    
    return milestones

def get_engagement_context(change):
    """
    Genera contexto para aumentar engagement según la tendencia.
    
    Args:
        change: Cambio en BTC (string con formato)
        
    Returns:
        dict: Emojis, pregunta y tono para el tweet
    """
    change_float = float(change.replace(",", ""))
    
    history = read_history()
    
    # Calcular si es el mayor cambio reciente
    is_biggest = False
    if len(history) >= 7:
        recent_changes = [abs(h["change"]) for h in history[-7:]]
        is_biggest = abs(change_float) > max(recent_changes)
    
    # Contexto según el cambio
    if change_float > 5000:
        return {
            "emoji": "🚀",
            "tone": "bullish",
            "question": "Bullish or Bearish? 👇",
            "prefix": "MASSIVE ACCUMULATION 📈" if is_biggest else "Strong Accumulation 💪"
        }
    elif change_float > 2000:
        return {
            "emoji": "📈",
            "tone": "positive",
            "question": "Is this the beginning of a trend? 🤔",
            "prefix": "Steady Growth ✨"
        }
    elif change_float > 0:
        return {
            "emoji": "➕",
            "tone": "neutral_positive",
            "question": "Accumulation continues... 👀",
            "prefix": "Small Increase"
        }
    elif change_float > -2000:
        return {
            "emoji": "➖",
            "tone": "neutral_negative",
            "question": "Just a dip or a trend? 📉",
            "prefix": "Minor Decrease"
        }
    elif change_float > -5000:
        return {
            "emoji": "📉",
            "tone": "negative",
            "question": "What's causing the outflow? 🤔",
            "prefix": "Notable Decrease ⚠️"
        }
    else:
        return {
            "emoji": "🔻",
            "tone": "bearish",
            "question": "Major outflow detected! Your thoughts? 💭",
            "prefix": "LARGE OUTFLOW 🚨" if is_biggest else "Significant Decrease"
        }

def get_trend_analysis():
    """
    Analiza la tendencia de los últimos días.
    
    Returns:
        dict: Análisis de tendencia o None
    """
    history = read_history()
    if len(history) < 3:
        return None
    
    recent = history[-5:] if len(history) >= 5 else history
    changes = [h["change"] for h in recent]
    
    positive = sum(1 for c in changes if c > 0)
    negative = sum(1 for c in changes if c < 0)
    
    avg_change = sum(changes) / len(changes)
    
    if positive > negative and avg_change > 1000:
        trend = "🔥 Strong accumulation trend"
    elif positive > negative:
        trend = "📊 Accumulation phase"
    elif negative > positive and avg_change < -1000:
        trend = "❄️ Outflow trend"
    elif negative > positive:
        trend = "📉 Distribution phase"
    else:
        trend = "🔄 Consolidation"
    
    return {
        "trend": trend,
        "positive_days": positive,
        "negative_days": negative,
        "avg_change": avg_change,
        "days_analyzed": len(recent)
    }
