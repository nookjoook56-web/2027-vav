import sys
import requests
import base64
import os

class VavooResolver:
    def __init__(self):
        # Paketten yakaladığınız imzasız katalog linki
        self.catalog_link = "https://shouurvki7jtfax.ngolpdkyoctjcddxshli469r.org/mediahubmx-catalog.json"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        })

    def fetch_all(self):
        """Katalog verisini çekmeye çalışır."""
        print(f"📡 Katalog verisi çekiliyor: {self.catalog_link}")
        
        payload = {
            "language": "tr", 
            "region": "TR", 
            "catalogId": "iptv",
            "filter": {"group": "Turkey"}
        }
        
        try:
            # İmza göndermeden doğrudan istek atıyoruz
            resp = self.session.post(self.catalog_link, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                print(f"✅ Başarılı! {len(items)} kanal alındı.")
                return items
            else:
                print(f"⚠️ Hata: {resp.status_code}")
                return []
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
            return []

    def resolve_url(self, ch):
        """URL'yi oynatılabilir formata çevirir."""
        url = ch.get("url", "")
        if url and not url.startswith("http"):
            try: url = base64.b64decode(url).decode('utf-8')
            except: pass
        if "vavoo.to" in url and "/play/" in url:
            url = url.replace("/play/", "/vavoo-iptv/play/")
        return url

if __name__ == "__main__":
    resolver = VavooResolver()
    if "--full-m3u" in sys.argv:
        all_data = resolver.fetch_all()
            
        if all_data:
            with open("vavoo_full.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for ch in all_data:
                    url = resolver.resolve_url(ch)
                    group = ch.get("group", "Genel")
                    f.write(f'#EXTINF:-1 group-title="{group}",{ch.get("name")}\n{url}\n')
            print("✅ Bitti! vavoo_full.m3u oluşturuldu.")
