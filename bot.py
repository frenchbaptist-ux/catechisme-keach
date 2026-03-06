import telebot
import json
import os
from flask import Flask
from threading import Thread

# 1. Configuration du Token
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. Mini-serveur Flask pour Render
app = Flask('')

@app.route('/')
def home():
    return "Bot Keach & Westminster en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Logique du bot
def load_data():
    base_path = os.path.dirname(__file__)
    # Pour l'instant on reste sur keach.json
    file_path = os.path.join(base_path, 'keach.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.message_handler(func=lambda message: True)
def handle_smart_response(message):
    if not message.text:
        return
    
    text = message.text.strip()
    bot_username = "@Keach_bot"
    is_private = message.chat.type == 'private'
    
    # INITIALISATION DE LA VARIABLE
    raw_num = ""

    # CAS A : En privé -> On accepte le chiffre pur (ex: "1")
    if is_private:
        raw_num = text.replace("/", "").strip()
    
    # CAS B : En groupe -> On exige la mention (ex: "@Keach_bot 1")
    elif bot_username in text:
        raw_num = text.replace(bot_username, "").replace("/", "").strip()
    
    # CAS C : En groupe sans mention -> On ignore (le bot se tait)
    else:
        return

    # TRAITEMENT DU NUMÉRO
    if raw_num.isdigit():
        try:
            data = load_data()
            if raw_num in data:
                question = data[raw_num]["question"]
                reponse = data[raw_num]["reponse"]
                texte_final = f"*{raw_num}. {question}*\n\n{reponse}"
                bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        except Exception as e:
            print(f"Erreur lors de la lecture du JSON : {e}")

# 4. Lancement
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Le bot est prêt et différencie le privé du public.")
    bot.infinity_polling()
