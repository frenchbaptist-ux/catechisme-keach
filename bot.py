import telebot
import json
import os

# 1. Récupération sécurisée du Token depuis les variables d'environnement de Render
# Note l'utilisation des guillemets ' ' à l'intérieur de la parenthèse
TOKEN = os.environ.get('BOT_TOKEN')

# On vérifie que le token est bien présent pour éviter de faire planter le bot
if not TOKEN:
    raise ValueError("La variable d'environnement BOT_TOKEN est manquante sur Render !")

bot = telebot.TeleBot(TOKEN)

# 2. Fonction pour charger le fichier JSON avec le bon encodage
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'keach.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 3. Gestionnaire de messages pour les chiffres (ex: "1", "2")
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_question(message):
    try:
        data = load_data()
        num = message.text.strip()

        if num in data:
            question = data[num]["question"]
            reponse = data[num]["reponse"]

            # Formatage : Gras pour le numéro et la question
            # On utilise les étoiles * * pour le mode Markdown
            texte_final = f"*{num}. {question}*\n\n{reponse}"
            
            bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Désolé, cette question n'est pas encore disponible.")
            
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        bot.reply_to(message, "Une erreur technique est survenue.")

# 4. Lancement du bot avec mode "infini" pour Render
if __name__ == "__main__":
    print("Le bot Keach est lancé et prêt !")
    bot.infinity_polling()
