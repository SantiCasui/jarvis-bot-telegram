import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TWELVE_API_KEY = "354c41fa243c4677a4491f35884d1fcb"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Bienvenido, señor Santiago. Estoy operativo. Puede solicitar cotizaciones escribiendo comandos como /precio btc, /precio oro o /precio eurusd.\n\n¿Cómo desea que lo asista hoy?"
    )

def get_price(symbol, source="coingecko"):
    if source == "coingecko":
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        r = requests.get(url)
        return r.json().get(symbol, {}).get("usd", "❌ No encontrado")
    elif source == "twelvedata":
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API_KEY}"
        r = requests.get(url)
        return r.json().get("price", "❌ No encontrado")
    return "❌ Fuente no válida"

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Señor, indique el activo. Por ejemplo: /precio btc o /precio oro.")
        return

    activo = args[0].lower()

    if activo == "btc":
        precio = get_price("bitcoin", source="coingecko")
        await update.message.reply_text(f"💰 BTC: ${precio}")
    elif activo == "oro":
        precio = get_price("XAU/USD", source="twelvedata")
        await update.message.reply_text(f"🪙 Oro: ${precio}")
    elif activo == "nasdaq":
        precio = get_price("IXIC", source="twelvedata")
        await update.message.reply_text(f"📈 Nasdaq: ${precio}")
    elif activo == "eurusd":
        precio = get_price("EUR/USD", source="twelvedata")
        await update.message.reply_text(f"💶 EUR/USD: ${precio}")
    elif activo == "eurjpy":
        precio = get_price("EUR/JPY", source="twelvedata")
        await update.message.reply_text(f"💴 EUR/JPY: ¥{precio}")
    else:
        await update.message.reply_text("❌ Activo no reconocido, señor.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.run_polling()
