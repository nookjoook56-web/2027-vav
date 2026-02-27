import requests
import base64
import os

def fetch_without_signature():
    # Görüntüde yakaladığınız katalog linki
    url = "https://shouurvki7jtfax.ngolpdkyoctjcddxshli469r.org/mediahubmx-catalog.json"
    
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "Accept": "application/json"
    }
    
    # İmza bilgisi göndermeden doğrudan istek atılıyor
    payload = {
        "language": "tr", 
        "region": "TR", 
        "filter": {"group": "Turkey"}
    }

    print("🕵️ İmzasız katalog denemesi yapılıyor...")
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code == 200:
            print("✅ Bağlantı başarılı! Liste çekiliyor...")
            return r.json().get("items", [])
        else:
            print(f"❌ Başarısız (Kod: {r.status_code})")
            return []
    except Exception as e:
        print(f"💥 Hata: {e}")
        return []
