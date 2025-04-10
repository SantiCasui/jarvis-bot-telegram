import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy tu JARVIS. Escribí /precio btc o /precio oro")

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Decime el activo: /precio btc o /precio oro")
        return

    activo = args[0].lower()
    if activo == "btc":
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url)
        data = r.json()
        precio = data["bitcoin"]["usd"]
        await update.message.reply_text(f"💰 Precio BTC: ${precio}")
    elif activo == "oro":
        await update.message.reply_text("🪙 Precio del oro próximamente disponible")
    else:
        await update.message.reply_text("Activo no reconocido")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.run_polling()
