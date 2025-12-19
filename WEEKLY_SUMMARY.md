# 📊 Resumen Semanal - Instrucciones

## ¿Qué hace?

Agrega un **resumen semanal automático** que se publica **cada domingo** con:
- Cambio neto de BTC y USD de la semana
- Días positivos vs negativos  
- Tasa de éxito semanal
- Tendencia (🚀 fuerte acumulación, 📈 positivo, 📉 negativo, etc.)

## 🧪 Probar SIN Publicar

```bash
python3 test_weekly.py
```

Esto:
- ✅ Obtiene datos reales de Bitbo.io
- ✅ Guarda en historial local
- ✅ Muestra cómo se vería el tweet
- ❌ NO publica nada en X

## ✅ Activar Resumen Semanal

### Paso 1: Reemplazar main.py

```bash
cp main.py main_backup.py
cp main_with_weekly.py main.py
```

### Paso 2: Commit y Push

```bash
git add .
git commit -m "Add weekly summary feature"
git push
```

### Paso 3: ¡Listo!

El bot ahora:
- ✅ Publica el update diario (como siempre)
- ✅ Guarda datos en historial cada día
- ✅ Publica resumen semanal **solo los domingos**

## 📝 Archivos Importantes

- `weekly_history.py` - Maneja el historial semanal (usa la misma estructura que `storage.py`)
- `main_with_weekly.py` - Main actualizado con resumen semanal
- `test_weekly.py` - Script de prueba (no publica)
- `weekly_data.json` - Historial guardado (automático, guardado en GitHub cache)

## ⚙️ Configuración

### Cambiar día de publicación

Edita `weekly_history.py`, línea 95:

```python
def should_post_weekly():
    return datetime.now().weekday() == 6  # 6 = Domingo
    # 0 = Lunes, 1 = Martes, ... 5 = Sábado
```

### Cambiar días de historial

Edita `weekly_history.py`, línea 45:

```python
# Guardar solo últimos 14 días
if len(history) > 14:
    history = history[-14:]
```

## ❓ FAQ

**¿Cuántos tweets va a publicar?**
- ~30 tweets al mes (1 diario)
- +4 resúmenes semanales al mes
- = ~34 tweets/mes (MUY dentro del límite gratuito de 500/mes)

**¿Qué pasa si no hay suficientes datos?**
Simplemente no publica el resumen. Necesita al menos 2 días de datos.

**¿Puedo desactivarlo?**
Sí, solo vuelve a usar `main_backup.py`:
```bash
cp main_backup.py main.py
```

## 📊 Ejemplo de Tweet Semanal

```
📊 WEEKLY SUMMARY
🚀 STRONG ACCUMULATION WEEK

📅 Dec 11, 2025 → Dec 17, 2025

📊 Net Change:
  🪙 +8,500.0 BTC
  💵 +$720,000,000

📈 Performance:
  ✅ Positive days: 5
  ❌ Negative days: 2
  📊 Success rate: 71%

What's your prediction for next week? 💭

#Bitcoin #BlackRock #IBIT #WeeklySummary
```

---

¡Eso es todo! 🚀 Simple, funcional y 100% gratis.
