"""
Simple weekly history tracker usando la misma estructura de storage.py
"""
from pathlib import Path
import json
from datetime import datetime

HISTORY_FILE = "weekly_data.json"

def add_daily_data(btc, usd, change, date):
    """
    Agrega datos diarios al historial semanal.
    
    Args:
        btc: Holdings en BTC (string con formato)
        usd: Valor en USD (string con formato)
        change: Cambio en BTC (string con formato)
        date: Fecha (string)
    """
    try:
        # Leer historial existente
        history = []
        file_path = Path(HISTORY_FILE)
        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # Convertir strings a números
        btc_float = float(btc.replace(",", ""))
        usd_float = float(usd.replace("$", "").replace(",", ""))
        change_float = float(change.replace(",", ""))
        
        # Crear nueva entrada
        entry = {
            "date": date,
            "btc": btc_float,
            "usd": usd_float,
            "change": change_float
        }
        
        # Agregar nueva entrada
        history.append(entry)
        
        # Guardar solo últimos 14 días
        if len(history) > 14:
            history = history[-14:]
        
        # Guardar archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
        
        print(f"✅ Datos agregados al historial semanal: {len(history)} días guardados")
        
    except Exception as e:
        print(f"⚠️ Error al guardar historial semanal: {e}")

def get_weekly_summary():
    """
    Calcula el resumen de los últimos 7 días.
    
    Returns:
        dict con resumen o None si no hay suficientes datos
    """
    try:
        file_path = Path(HISTORY_FILE)
        if not file_path.is_file():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if len(history) < 2:
            return None
        
        # Tomar últimos 7 días (o los que haya)
        recent = history[-7:] if len(history) >= 7 else history
        
        first = recent[0]
        last = recent[-1]
        
        # Calcular cambios
        btc_change = last["btc"] - first["btc"]
        
        # Contar días positivos/negativos
        positive_days = sum(1 for entry in recent if entry["change"] > 0)
        negative_days = sum(1 for entry in recent if entry["change"] < 0)
        
        return {
            "start_date": first["date"],
            "end_date": last["date"],
            "current_btc": last["btc"],  # Holdings actuales
            "btc_change": btc_change,
            "positive_days": positive_days,
            "negative_days": negative_days,
            "days": len(recent)
        }
        
    except Exception as e:
        print(f"⚠️ Error al calcular resumen semanal: {e}")
        return None

def should_post_weekly():
    """
    Determina si es domingo (día para resumen semanal).
    
    Returns:
        bool: True si es domingo
    """
    return datetime.now().weekday() == 6  # 6 = Domingo
