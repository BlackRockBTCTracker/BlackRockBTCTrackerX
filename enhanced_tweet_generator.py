from history_storage import (
    get_engagement_context, 
    check_milestones, 
    get_trend_analysis,
    get_weekly_summary
)
from datetime import datetime

def generate_enhanced_daily_tweet(btc, usd, change, date):
    """
    Genera un tweet mejorado con engagement hooks.
    
    Args:
        btc: Holdings en BTC
        usd: Valor en USD
        change: Cambio en BTC
        date: Fecha
        
    Returns:
        str: Tweet formateado con emojis y engagement hooks
    """
    # Obtener contexto de engagement
    context = get_engagement_context(change)
    
    # Formatear el cambio con + si no tiene signo negativo
    formatted_change = change if change.startswith('-') else f"+{change}"
    
    # Obtener análisis de tendencia si está disponible
    trend = get_trend_analysis()
    trend_line = f"\n📊 {trend['trend']}" if trend else ""
    
    # Construir el mensaje con engagement
    message = (
        f"{context['emoji']} {context['prefix']}\n\n"
        f"BlackRock Bitcoin ETF (IBIT) Update – {date}\n\n"
        f"🪙 Holdings: {btc} BTC\n"
        f"💵 USD Value: {usd}\n"
        f"➕ Change: {formatted_change} BTC"
        f"{trend_line}\n\n"
        f"💬 {context['question']}\n\n"
        f"📊 Source: Bitbo.io\n"
        f"#Bitcoin #BlackRock #IBIT #BTCETF"
    )
    
    return message

def generate_milestone_tweet(milestone_data):
    """
    Genera un tweet especial para milestones alcanzados.
    
    Args:
        milestone_data: Dict con información del milestone
        
    Returns:
        str: Tweet formateado para milestone
    """
    emoji_map = {
        "btc": "🎯",
        "usd": "💰",
        "percentage": "📊"
    }
    
    emoji = emoji_map.get(milestone_data["type"], "🎉")
    
    message = (
        f"{emoji} MILESTONE ALERT! {emoji}\n\n"
        f"{milestone_data['message']}\n\n"
        f"BlackRock's IBIT continues to be a major player in the Bitcoin ETF space.\n\n"
        f"What does this mean for Bitcoin adoption? 🤔\n\n"
        f"#Bitcoin #BlackRock #IBIT #Milestone #Crypto"
    )
    
    return message

def generate_weekly_summary_tweet(summary):
    """
    Genera un tweet de resumen semanal.
    
    Args:
        summary: Dict con estadísticas de la semana
        
    Returns:
        str: Tweet formateado con resumen semanal
    """
    # Determinar tendencia general
    if summary["btc_change"] > 5000:
        trend_emoji = "🚀"
        trend_text = "STRONG ACCUMULATION WEEK"
    elif summary["btc_change"] > 0:
        trend_emoji = "📈"
        trend_text = "Positive Week"
    elif summary["btc_change"] > -5000:
        trend_emoji = "📉"
        trend_text = "Slight Decrease Week"
    else:
        trend_emoji = "🔻"
        trend_text = "OUTFLOW WEEK"
    
    # Formatear cambios
    btc_change_str = f"+{summary['btc_change']:,.1f}" if summary['btc_change'] >= 0 else f"{summary['btc_change']:,.1f}"
    usd_change_str = f"+${summary['usd_change']:,.0f}" if summary['usd_change'] >= 0 else f"-${abs(summary['usd_change']):,.0f}"
    
    # Calcular porcentaje de días positivos
    total_days = summary['positive_days'] + summary['negative_days']
    positive_pct = (summary['positive_days'] / total_days * 100) if total_days > 0 else 0
    
    message = (
        f"{trend_emoji} BI-WEEKLY SUMMARY {trend_emoji}\n"
        f"{trend_text}\n\n"
        f"📅 Period: {summary['start_date']} → {summary['end_date']}\n\n"
        f"📊 Net Change:\n"
        f"  🪙 {btc_change_str} BTC\n"
        f"  💵 {usd_change_str}\n\n"
        f"📈 Performance:\n"
        f"  ✅ Positive days: {summary['positive_days']}\n"
        f"  ❌ Negative days: {summary['negative_days']}\n"
        f"  📊 Success rate: {positive_pct:.0f}%\n\n"
        f"💭 What are your thoughts on the trend?\n\n"
        f"#Bitcoin #BlackRock #IBIT #BiWeeklySummary"
    )
    
    return message

def generate_trend_analysis_tweet():
    """
    Genera un tweet con análisis de tendencia actual.
    
    Returns:
        str or None: Tweet con análisis o None si no hay suficientes datos
    """
    trend = get_trend_analysis()
    if not trend:
        return None
    
    avg_change_str = f"+{trend['avg_change']:,.0f}" if trend['avg_change'] >= 0 else f"{trend['avg_change']:,.0f}"
    
    message = (
        f"📊 TREND ANALYSIS - Last {trend['days_analyzed']} Days\n\n"
        f"{trend['trend']}\n\n"
        f"📈 Positive days: {trend['positive_days']}\n"
        f"📉 Negative days: {trend['negative_days']}\n"
        f"💹 Avg daily change: {avg_change_str} BTC\n\n"
        f"Keep watching for updates! 👀\n\n"
        f"#Bitcoin #BlackRock #IBIT #Analysis"
    )
    
    return message

def should_post_weekly_summary():
    """
    Determina si es momento de publicar el resumen quincenal.
    Se publica el 1er y 3er domingo de cada mes para no saturar.
    
    Returns:
        bool: True si debe publicar el resumen
    """
    now = datetime.now()
    
    # Verificar si es domingo (6 en Python)
    is_sunday = now.weekday() == 6
    
    # Verificar si es entre 8-10 AM
    is_morning = now.hour >= 8 and now.hour <= 10
    
    # Verificar si es el 1er o 3er domingo del mes
    day = now.day
    is_first_or_third_sunday = (1 <= day <= 7) or (15 <= day <= 21)
    
    return is_sunday and is_morning and is_first_or_third_sunday

def generate_all_tweets(btc, usd, change, date):
    """
    Genera todos los tweets posibles para la situación actual.
    
    Args:
        btc: Holdings en BTC
        usd: Valor en USD
        change: Cambio en BTC
        date: Fecha
        
    Returns:
        dict: Diccionario con todos los tweets generados
    """
    tweets = {}
    
    # 1. Tweet diario principal (siempre)
    tweets["daily"] = generate_enhanced_daily_tweet(btc, usd, change, date)
    
    # 2. Milestones (si se alcanzaron)
    milestones = check_milestones(btc, usd)
    if milestones:
        tweets["milestones"] = [generate_milestone_tweet(m) for m in milestones]
    
    # 3. Resumen semanal (si corresponde)
    if should_post_weekly_summary():
        summary = get_weekly_summary()
        if summary:
            tweets["weekly_summary"] = generate_weekly_summary_tweet(summary)
    
    return tweets
