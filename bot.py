import telebot
import json
import os
from flask import Flask
from threading import Thread

# 1. Configuration du Token
TOKEN = os.environ.get('BOT_TOKEN')
# On active explicitement la lecture des messages
bot = telebot.TeleBot(TOKEN, threaded=True)

# 2. Mini-serveur Flask (pour Render)
app = Flask('')

@app.route('/')
def home():
    return "Bot Keach est en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Logique du bot
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'keach.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# On écoute tous les messages texte
@bot.message_handler(content_types=['text'])
def handle_message(message):
    # On nettoie le texte (enlève le / et les espaces)
    raw_text = message.text.strip().replace('/', '')
    
    if raw_text.isdigit():
        try:
            data = load_data()
            if raw_text in data:
                question = data[raw_text]["question"]
                reponse = data[raw_text]["reponse"]
                
                # Formatage propre
                texte_final = f"*{raw_text}. {question}*\n\n{reponse}"
                bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        except Exception as e:
            print(f"Erreur JSON : {e}")

# 4. Lancement
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot Keach prêt pour les groupes !")
    bot.infinity_polling(allowed_updates=["message"])
