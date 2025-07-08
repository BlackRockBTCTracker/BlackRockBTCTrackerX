from pathlib import Path

def read_last_value():
    """
    Lee el último valor guardado en el archivo local.
    
    Returns:
        str or None: El último valor guardado (puede ser fecha o valor numérico),
                    o None si no existe o hay un error.
    """
    try:
        file_path = Path("last_value.txt")
        if file_path.is_file():
            content = file_path.read_text(encoding='utf-8').strip()
            if content:  # Solo devolver si hay contenido
                return content
    except Exception as e:
        print(f"⚠️ Error al leer el archivo de valor anterior: {e}")
    return None

def write_last_value(value):
    """
    Guarda el último valor (fecha) en el archivo local.
    
    Args:
        value: El valor a guardar (se convertirá a string).
    """
    if value is None:
        print("⚠️ Intento de guardar un valor nulo")
        return
        
    value = str(value).strip()
    if not value:
        print("⚠️ Intento de guardar un valor vacío")
        return
    
    # Guarda en el archivo local
    try:
        file_path = Path("last_value.txt")
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Asegura que el directorio exista
        file_path.write_text(value, encoding='utf-8')
        print(f"✅ Valor guardado en el archivo: {value}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar el valor en el archivo: {e}")
        raise
