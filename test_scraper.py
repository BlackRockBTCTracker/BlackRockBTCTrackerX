from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
import os
import requests
from bs4 import BeautifulSoup

def test_scraper():
    print("=" * 50)
    print("🧪 TEST: Obteniendo datos de BlackRock")
    print("=" * 50)
    
    # Primero ver el HTML raw
    print("\n🔍 Inspeccionando HTML del sitio...")
    url = "https://bitbo.io/treasuries/blackrock-ibit/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar todos los elementos con right-align
    print("\n📋 Elementos 'right-align' encontrados:")
    for elem in soup.find_all("td", class_="right-align"):
        classes = elem.get("class", [])
        text = elem.get_text(strip=False)
        print(f"   Clases: {classes}")
        print(f"   Texto completo: '{text}'")
        print(f"   HTML: {elem}")
        print("   ---")
    
    try:
        # Obtener datos del scraper
        btc, usd, change, date = get_blackrock_data()
        
        print(f"\n📊 Datos obtenidos:")
        print(f"   BTC: {btc}")
        print(f"   USD: {usd}")
        print(f"   Change: {change}")
        print(f"   Date: {date}")
        
        print(f"\n🔍 Análisis del cambio:")
        print(f"   Valor raw: '{change}'")
        print(f"   Tipo: {type(change)}")
        print(f"   Empieza con '-': {change.startswith('-')}")
        print(f"   Empieza con '+': {change.startswith('+')}")
        
        # Crear directorio de prueba
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar imagen
        print(f"\n🖼️ Generando imagen...")
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)
        print(f"✅ Imagen generada: {output_path}")
        
        # Mostrar cómo se vería el tweet
        formatted_change = change if change.startswith('-') else f"+{change}"
        print(f"\n📝 Preview del tweet:")
        print(f"   Change formateado: {formatted_change}")
        message = (
            f"BlackRock Bitcoin ETF (IBIT) Update – {date}\n\n"
            f"🪙 Holdings: {btc} BTC\n"
            f"💵 USD Value: {usd}\n"
            f"➕ Change: {formatted_change} BTC\n\n"
            f"📊 Source: http://Bitbo.io\n\n"
            f"#Bitcoin #BlackRock #IBIT #BTCETF"
        )
        print("\n" + "=" * 50)
        print(message)
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scraper()
