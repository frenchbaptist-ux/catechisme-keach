import telebot
import json
import os
from flask import Flask
from threading import Thread

# 1. Configuration du Token
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. Mini-serveur Flask pour garder Render content
app = Flask('')

@app.route('/')
def home():
    return "Bot Keach est en ligne !"

def run_flask():
    # Render passe le port via une variable d'environnement
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Logique du bot (chargement JSON)
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'keach.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_question(message):
    try:
        data = load_data()
        num = message.text.strip()
        if num in data:
            question = data[num]["question"]
            reponse = data[num]["reponse"]
            texte_final = f"*{num}. {question}*\n\n{reponse}"
            bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Question non disponible.")
    except Exception as e:
        bot.reply_to(message, "Erreur technique.")

# 4. Lancement simultané
if __name__ == "__main__":
    # On lance Flask dans un thread séparé
    t = Thread(target=run_flask)
    t.start()
    
    print("Serveur Flask lancé, démarrage du bot...")
    # On lance le bot sur le thread principal
    bot.infinity_polling()
