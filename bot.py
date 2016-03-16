import telebot
import json

# Create bot with its token
with open("./links.token", "r") as TOKEN:
  bot = telebot.TeleBot(TOKEN.readline().strip())

# Files used
with open('./data/data.json', 'r') as j:
  data = json.load(j)
  start_message = data['start']

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


def isUserAnswer(user, userTracking):
  if user in userTracking.keys():
    return True
  else:
    return False


def saveUser(user):
  with open('./data/links.json', 'r') as links_json:
    links = json.load(links_json)
  if not str(user) in links.keys():
    links[str(user)] = {}
    with open('./data/links.json', 'w') as jsave:
      json.dump(links, jsave)


def refresh_links(user):
  links = json.load(open('./data/links.json'))
  link_list  = "Links saved:\n\n"

  i = 1
  for majorkey, linkdict in links.items():
    if str(majorkey) == str(user):
      if not bool(links[str(user)]):
          return "Not saved links mate!"
      for key in linkdict:
        link_list += str(i) + " - #" + linkdict[key] + "  ->  "
        link_list += key + "\n"
        i = i + 1
      return link_list
  return "Not saved links mate!"

def remove_links(user):
  links = json.load(open('./data/links.json'))

  i = 1
  for majorkey, linkdict in links.items():
    if str(majorkey) == str(user):
      if not bool(links[str(user)]):
        return "Not saved links mate!"
      links[str(user)] = {}
      with open('./data/links.json', 'w') as jsave:
        json.dump(links, jsave)
      return "All links removed!"
    i = i + 1

def save_link(user, link, tag):
  with open('./data/links.json', 'r') as links_json:
    links = json.load(links_json)

  links[str(user)][link] = tag
  with open('./data/links.json', 'w') as jsave:
    json.dump(links, jsave)

# Set listener to print messages
bot.set_update_listener(listener)

# Ignore old messages
bot.skip_pending = True

print("Running...")

# Handlers
@bot.message_handler(commands=['start'])
def send_start(message):
  bot.reply_to(message, start_message)

@bot.message_handler(commands=['list'])
def send_links(message):
  links = refresh_links(message.chat.id)
  bot.send_message(message.chat.id, links)

userTracking = {}
@bot.message_handler(commands=['save'])
def send_save_link(message):
  saveUser(message.chat.id)
  if message.text == '/save' or message.text == '/save@saveLinks_bot':
    bot.send_message(message.chat.id, "What link de you want to store?")
    userTracking[message.from_user.id] = message.chat.first_name
  else:
    url = message.text.split(' ')[1]
    tag = message.text.split(' ')[2]
    save_link(message.chat.id, url, tag)
    bot.reply_to(message, "Link saved!")

@bot.message_handler(func=lambda message: isUserAnswer(message.from_user.id, userTracking))
def catch_save_link(message):
  url = message.text.split(' ')[0]
  tag = message.text.split(' ')[1]
  save_link(message.chat.id, url, tag)
  bot.reply_to(message, "Link saved!")

@bot.message_handler(commands=['removeall'])
def send_remove_links(message):
  cid = message.chat.id
  saveUser(cid)
  removeMessage = remove_links(cid)
  bot.reply_to(message, removeMessage)

# Start the bot
bot.polling()
