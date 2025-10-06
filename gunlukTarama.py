import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime

# Telegram Bot ayarları
TELEGRAM_TOKEN = "8256592463:AAHlJ3BQSvwUDOQuKCYAhKwAwMMWUFJXE4o"
CHAT_ID = "1008660822"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# BIST 100 sembol listesi
SYMBOLS = [
    "ASELS.IS", "GARAN.IS", "THYAO.IS", "KCHOL.IS", "ENKAI.IS", "ISCTR.IS",
    "TUPRS.IS", "FROTO.IS", "AKBNK.IS", "BIMAS.IS", "YKBNK.IS", "DSTKF.IS",
    "VAKBN.IS", "TCELL.IS", "EREGL.IS", "HALKB.IS", "SAHOL.IS", "TTKOM.IS",
    "SASA.IS", "CCOLA.IS", "TOASO.IS", "SISE.IS", "PGSUS.IS", "GUBRF.IS",
    "OYAKC.IS", "ASTOR.IS", "TURSG.IS", "ENERY.IS", "ENJSA.IS", "ARCLK.IS",
    "TAVHL.IS", "AEFES.IS", "KOZAL.IS", "MGROS.IS", "PASEU.IS", "EKGYO.IS",
    "MAGEN.IS", "MPARK.IS", "ISMEN.IS", "BRYAT.IS", "GRTHO.IS", "AGHOL.IS",
    "OTKAR.IS", "BRSAN.IS", "TABGD.IS", "TTRAK.IS", "GENIL.IS", "RALYH.IS",
    "PETKM.IS", "EFORC.IS", "AKSEN.IS", "DOHOL.IS", "AKSA.IS", "CIMSA.IS",
    "ANSGR.IS", "ULKER.IS", "CLEBI.IS", "TSKB.IS", "ALARK.IS", "GRSEL.IS",
    "KOZAA.IS", "DOAS.IS", "HEKTS.IS", "TKFEN.IS", "KRDMD.IS", "MAVI.IS",
    "KTLEV.IS", "KCAER.IS", "EGEEN.IS", "BTCIM.IS", "AVPGY.IS", "BSOKE.IS",
    "KONTR.IS", "CWENE.IS", "OBAMS.IS", "MIATK.IS", "SOKM.IS", "GESAN.IS",
    "IPEKE.IS", "GSRAY.IS", "KUYAS.IS", "EUPWR.IS", "ZOREN.IS", "SMRTG.IS",
    "ALFAS.IS", "ALTNY.IS", "SKBNK.IS", "CANTE.IS", "FENER.IS", "IEYHO.IS",
    "LMKDC.IS", "BINHO.IS", "YEOTK.IS", "VESTL.IS", "BERA.IS", "REEDR.IS",
    "TUREX.IS", "ODAS.IS", "BALSU.IS", "GLRMK.IS"
]

def calculate_rsi(data, periods=31):
    """RSI hesaplama fonksiyonu"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def send_telegram_message(message):
    """Telegram mesaj gönderme fonksiyonu"""
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ Telegram hatası: {str(e)}")

def main():
    print("🚀 BIST 100 RSI Tarayıcı Başlatıldı")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Toplam {len(SYMBOLS)} hisse analiz edilecek\n")

    results = []

    for idx, symbol in enumerate(SYMBOLS, 1):
        try:
            print(f"[{idx}/{len(SYMBOLS)}] {symbol} analiz ediliyor...", end=" ")

            # Haftalık veriyi çek
            stock = yf.Ticker(symbol)
            df = stock.history(period="2y", interval="1wk")

            if df.empty or len(df) < 32:
                print("❌ Yetersiz veri")
                continue

            # RSI ve SMA hesapla
            df['RSI'] = calculate_rsi(df['Close'], periods=31)
            df['RSI_SMA'] = df['RSI'].rolling(window=31).mean()

            latest = df.iloc[-1]
            prev = df.iloc[-2]

            # Koşul: SMA 51-55 arasında + RSI önce <51 iken şimdi 51-55 arasında
            if (51 <= latest['RSI_SMA'] <= 55) and (prev['RSI'] < 51) and (51 <= latest['RSI'] <= 55):
                results.append({
                    "symbol": symbol.replace('.IS', ''),
                    "rsi": float(latest['RSI']),
                    "sma": float(latest['RSI_SMA'])
                })
                print("✅ Koşul sağlandı")
            else:
                print("⚪ Koşul sağlanmadı")

        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    # Özet
    print("\n" + "="*50)
    print("📊 ANALIZ SONUÇLARI")
    print("="*50)
    print(f"🎯 RSI<51'den çıkıp 51-55 aralığında + SMA 51-55: {len(results)} hisse")
    print("="*50 + "\n")

    # Telegram mesajı
    message_parts = []
    message_parts.append(f"*📈 BIST 100 RSI Tarayıcı*")
    message_parts.append(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    message_parts.append(f"*🎯 RSI <51'den çıkıp 51-55 aralığında & SMA 51-55 ({len(results)} hisse):*")

    if results:
        for stock in results:
            message_parts.append(f"• {stock['symbol']}: RSI {stock['rsi']:.2f} | SMA {stock['sma']:.2f}")
    else:
        message_parts.append("Koşulu sağlayan hisse yok")

    message = "\n".join(message_parts)
    send_telegram_message(message)

    print("✅ Analiz tamamlandı!")

if __name__ == "__main__":
    main()
