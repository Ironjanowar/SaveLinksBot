import telebot
import json

# Create bot with its token
with open("./links.token", "r") as TOKEN:
  bot = telebot.TeleBot(TOKEN.readline().strip())

# Functions used
def listener(messages):
  # When new messages arrive TeleBot will call this function.
  for m in messages:
    if m.content_type == 'text':
      # Prints the sent message to the console
      if m.chat.type == 'private':
        print ("Chat -> " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
      else:
        print ("Group -> " + str(m.chat.title) + " [" + str(m.chat.id) + "]: " + m.text)

# Set listener to print messages
bot.set_update_listener(listener)

# Ignore old messages
bot.skip_pending = True

print("Running...")

# Handlers

@bot.message_handler(commands=['start'])
def send_start(message):
  bot.reply_to(message, "Well hello!")

# Start the bot
bot.polling()
