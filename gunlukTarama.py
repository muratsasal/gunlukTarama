import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime

# Telegram Bot ayarları
TELEGRAM_TOKEN = "8256592463:AAHlJ3BQSvwUDOQuKCYAhKwAwMMWUFJXE4o"
CHAT_ID = "-1003198250448"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# BIST 100 sembol listesi
SYMBOLS = [
    "A1CAP.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS",
    "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS",
    "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFIS.IS", "AKFYE.IS", "AKGRT.IS",
    "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "ALARK.IS", "ALBRK.IS",
    "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS",
    "ALKLC.IS", "ALTNY.IS", "ALVES.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS",
    "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARMGD.IS",
    "ARSAN.IS", "ARTMS.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS",
    "ATAKP.IS", "ATATP.IS", "AVPGY.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS",
    "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAHKM.IS", "BAKAB.IS",
    "BALSU.IS", "BANVT.IS", "BARMA.IS", "BASCM.IS", "BASGZ.IS", "BEGYO.IS",
    "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS",
    "BIGEN.IS", "BIMAS.IS", "BINBN.IS", "BINHO.IS", "BIOEN.IS", "BIZIM.IS",
    "BJKAS.IS", "BLCYT.IS", "BMSTL.IS", "BOBET.IS", "BORLS.IS", "BORSK.IS",
    "BOSSA.IS", "BRISA.IS", "BRKVY.IS", "BRLSM.IS", "BRSAN.IS", "BRYAT.IS",
    "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BULGS.IS", "BVSAN.IS", "CANTE.IS",
    "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CEMZY.IS",
    "CGCAM.IS", "CIMSA.IS", "CLEBI.IS", "CMBTN.IS", "CMENT.IS", "CONSE.IS",
    "CRFSA.IS", "CUSAN.IS", "CVKMD.IS", "CWENE.IS", "DAGI.IS", "DAPGM.IS",
    "DARDL.IS", "DCTTR.IS", "DERHL.IS", "DERIM.IS", "DESA.IS", "DEVA.IS",
    "DGATE.IS", "DGGYO.IS", "DGNMO.IS", "DITAS.IS", "DMRGD.IS", "DNISI.IS",
    "DOAS.IS", "DOBUR.IS", "DOCO.IS", "DOFER.IS", "DOHOL.IS", "DOKTA.IS",
    "DSTKF.IS", "DURKN.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS",
    "ECZYT.IS", "EDIP.IS", "EFORC.IS", "EGEEN.IS", "EGEGY.IS", "EGEPO.IS",
    "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKOS.IS", "EKSUN.IS",
    "ELITE.IS", "EMKEL.IS", "ENDAE.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS",
    "ENSRI.IS", "ENTRA.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ESCAR.IS",
    "ESCOM.IS", "ESEN.IS", "EUPWR.IS", "EUREN.IS", "EYGYO.IS", "FENER.IS",
    "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FROTO.IS", "FZLGY.IS",
    "GARAN.IS", "GARFA.IS", "GEDIK.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS",
    "GESAN.IS", "GIPTA.IS", "GLCVY.IS", "GLRMK.IS", "GLRYH.IS", "GLYHO.IS",
    "GMTAS.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRSEL.IS",
    "GRTHO.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GUNDG.IS", "GWIND.IS",
    "GZNMI.IS", "HALKB.IS", "HATSN.IS", "HEDEF.IS", "HEKTS.IS", "HLGYO.IS",
    "HOROZ.IS", "HRKET.IS", "HTTBT.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS",
    "IEYHO.IS", "IHAAS.IS", "IHLAS.IS", "IHLGM.IS", "IMASM.IS", "INDES.IS",
    "INFO.IS", "INGRM.IS", "INTEK.IS", "INTEM.IS", "INVEO.IS", "INVES.IS",
    "IPEKE.IS", "ISBIR.IS", "ISBTR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS",
    "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISKUR.IS", "ISMEN.IS", "ISSEN.IS",
    "IZENR.IS", "IZFAS.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS",
    "KARSN.IS", "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KBORU.IS", "KCAER.IS",
    "KCHOL.IS", "KENT.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLKIM.IS",
    "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KLYPV.IS",
    "KMPUR.IS", "KNFRT.IS", "KOCMT.IS", "KONKA.IS", "KONTR.IS", "KONYA.IS",
    "KOPOL.IS", "KORDS.IS", "KOTON.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS",
    "KRDMB.IS", "KRDMD.IS", "KRONT.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS",
    "KTSKR.IS", "KUTPO.IS", "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS",
    "LIDER.IS", "LIDFA.IS", "LILAK.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS",
    "LOGO.IS", "LRSHO.IS", "LUKSK.IS", "LYDHO.IS", "LYDYE.IS", "MAALT.IS",
    "MACKO.IS", "MAGEN.IS", "MAKTK.IS", "MARBL.IS", "MARTI.IS", "MAVI.IS",
    "MEDTR.IS", "MEGMT.IS", "MEKAG.IS", "MERCN.IS", "MERIT.IS", "METUR.IS",
    "MGROS.IS", "MHRGY.IS", "MIATK.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS",
    "MOGAN.IS", "MOPAS.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS",
    "MTRKS.IS", "NATEN.IS", "NETAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS",
    "NUHCM.IS", "OBAMS.IS", "ODAS.IS", "ODINE.IS", "OFSYM.IS", "ONCSM.IS",
    "ONRYT.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OTKAR.IS", "OTTO.IS",
    "OYAKC.IS", "OYYAT.IS", "OZATD.IS", "OZKGY.IS", "OZSUB.IS", "OZYSR.IS",
    "PAGYO.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS",
    "PCILT.IS", "PEKGY.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS",
    "PINSU.IS", "PKENT.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS",
    "POLTK.IS", "PRKAB.IS", "PRKME.IS", "PSGYO.IS", "QNBFK.IS", "QNBTR.IS",
    "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RGYAS.IS", "RUZYE.IS",
    "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SANFM.IS", "SANKO.IS",
    "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGMN.IS", "SEGYO.IS",
    "SELEC.IS", "SERNT.IS", "SISE.IS", "SKBNK.IS", "SKYMD.IS", "SMRTG.IS",
    "SMRVA.IS", "SNGYO.IS", "SNICA.IS", "SNPAM.IS", "SOKE.IS", "SOKM.IS",
    "SONME.IS", "SRVGY.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TABGD.IS",
    "TARKM.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS",
    "TCKRC.IS", "TEHOL.IS", "TEKTU.IS", "TERA.IS", "TEZOL.IS", "TGSAS.IS",
    "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TMPOL.IS", "TMSN.IS", "TNZTP.IS",
    "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRHOL.IS", "TRILC.IS", "TSGYO.IS",
    "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS",
    "TUREX.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULKER.IS", "ULUFA.IS",
    "ULUSE.IS", "ULUUN.IS", "UNLU.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS",
    "VAKKO.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", "VESTL.IS",
    "VKGYO.IS", "VRGYO.IS", "VSNMD.IS", "YAPRK.IS", "YATAS.IS", "YBTAS.IS",
    "YEOTK.IS", "YGGYO.IS", "YIGIT.IS", "YKBNK.IS", "YUNSA.IS", "YYLGD.IS",
    "ZOREN.IS", "ZRGYO.IS"
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
    message_parts.append(f"*📈 BIST 100 kısa vade yükseliş potansiyeli olanlar*")
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


