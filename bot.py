import telebot
import json
import os

# Ton token est déjà défini
bot = telebot.TeleBot(BOT_TOKEN)

# Fonction pour charger le fichier JSON
def load_data():
    # On utilise un chemin relatif pour que cela fonctionne sur Render
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

            # Formatage : **Numéro. Question** (en gras) suivi de la réponse
            # On utilise le MarkdownV2 ou Markdown pour le gras
            texte_final = f"*{num}. {question}*\n\n{reponse}"
            
            bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Désolé, cette question n'est pas encore disponible dans le catéchisme.")
            
    except Exception as e:
        print(f"Erreur : {e}")
        bot.reply_to(message, "Une erreur est survenue lors de la lecture du catéchisme.")

# Lancement du bot
if __name__ == "__main__":
    print("Bot Keach en cours d'exécution...")
    bot.infinity_polling()
