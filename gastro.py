import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Token del bot (de BotFather)
TELEGRAM_TOKEN = "8363379423:AAERPXRai25SFiyg1pjghKqm_pGlvXQjIRw"

# Cargar base de datos de enfermedades desde JSON
with open("enfermedades.json", "r", encoding="utf-8") as f:
    enfermedades = json.load(f)

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu asistente sobre enfermedades gastrointestinales.\n"
        "Escribe el nombre de una enfermedad (ej: gastritis, colitis, úlcera, reflujo) "
        "o usa /lista para ver todas las disponibles."
    )

# Nueva función: mostrar lista de enfermedades
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombres = sorted(enfermedades.keys())  # orden alfabético
    lista_texto = "📖 Enfermedades disponibles:\n\n" + "\n".join([f"- {n.title()}" for n in nombres])
    await update.message.reply_text(lista_texto)

# Función para responder consultas
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    consulta = update.message.text.lower().strip()

    if consulta in enfermedades:
        enfermedad = enfermedades[consulta]
        respuesta = (
            f"📌 *{consulta.title()}*\n\n"
            f"📝 Descripción: {enfermedad['descripcion']}\n"
            f"🤒 Síntomas: {enfermedad['sintomas']}\n"
            f"✅ Prevención: {enfermedad['prevencion']}\n"
            f"⚠️ Cuándo acudir al médico: {enfermedad['cuandollamar']}"
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
    app.add_handler(CommandHandler("lista", lista))  # nuevo comando
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot ejecutandose en Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
