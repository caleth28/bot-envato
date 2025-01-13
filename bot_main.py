import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from get_envato_link import get_envato_link

# Tu token de BotFather
TELEGRAM_BOT_TOKEN = "7480783049:AAHXg-v_GBRC7MwSorGGTqfKS80tVvo03Mk"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start -> mensaje de bienvenida
    """
    await update.message.reply_text(
        "¡Hola! Envíame un enlace de Envato Elements y trataré de devolverte el enlace directo (envatousercontent.com)."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja el texto que no sea /start.
    Si contiene "envato.com", obtenemos el link temporal y lo enviamos.
    """
    text = update.message.text.strip()

    if "envato.com" in text:
        await update.message.reply_text("Procesando tu enlace, espera unos segundos...")

        # Llamar a la función que obtiene el link temporal
        link_temporal = get_envato_link(text)

        await update.message.reply_text(
            f"Resultado:\n{link_temporal}\n"
            "Haz clic en este enlace para descargarlo en tu PC (mientras esté válido)."
        )
    else:
        await update.message.reply_text(
            "No detecto un enlace de Envato. Mándame algo como:\n"
            "https://elements.envato.com/es/text-animation-toolkit-D8HAYMX"
        )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))
    # Cualquier texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot iniciado. Esperando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()
