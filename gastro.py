import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Token desde variable de entorno
TELEGRAM_TOKEN = os.getenv("8363379423:AAERPXRai25SFiyg1pjghKqm_pGlvXQjIRw")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ ERROR: No se encontró el token. Define la variable de entorno TELEGRAM_TOKEN.")

# Cargar base de datos de enfermedades
with open("enfermedades.json", "r", encoding="utf-8") as f:
    enfermedades = json.load(f)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu asistente sobre enfermedades gastrointestinales.\n"
        "Escribe el nombre de una enfermedad o usa /lista para ver todas las disponibles."
    )

# Comando /lista
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombres = sorted(enfermedades.keys())
    lista_texto = "📖 Enfermedades disponibles:\n\n" + "\n".join([f"- {n.title()}" for n in nombres])
    await update.message.reply_text(lista_texto)

# Responder consultas
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    consulta = update.message.text.lower().strip()

    if consulta in enfermedades:
        e = enfermedades[consulta]
        respuesta = (
            f"📌 *{consulta.title()}*\n\n"
            f"📝 Descripción: {e['descripcion']}\n"
            f"🤒 Síntomas: {e['sintomas']}\n"
            f"✅ Prevención: {e['prevencion']}\n"
            f"⚠️ Cuándo acudir al médico: {e['cuandollamar']}"
        )
        await update.message.reply_text(respuesta, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❓ No tengo información sobre esa enfermedad.\n"
            "Usa /lista para ver todas las disponibles."
        )

# Main
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("✅ Bot ejecutándose en Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()

