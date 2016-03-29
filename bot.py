import telebot
import json
import os.path as path

# Create bot with its token
with open("./links.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Check if everything is all right
if not path.isfile('./data/links.json'):
    with open('./data/links.json', 'w') as linksFile:
        linksFile.write('{}')
        linksFile.close()

# Files used
with open('./data/data.json', 'r') as j:
    data = json.load(j)
    start_message = data['start']

with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)

# Functions used


def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
        return False


def listener(messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        if m.content_type == 'text':
            # Prints the sent message to the console
            if m.chat.type == 'private':
                print("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
            else:
                print("Group -> " + str(m.chat.title) +
                      " [" + str(m.chat.id) + "]: " + m.text)


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
    link_list = "Links saved:\n\n"

    i = 1
    for majorkey, linkdict in links.items():
        if str(majorkey) == str(user):
            if not bool(links[str(user)]):
                return "Not saved links!"
            for key in linkdict:
                value = linkdict[key]
                value = "#{}".format(value) if not value.startswith("#") and value != "" else value
                link_list += "{}. {} -> {}\n".format(i, value, key)
                # link_list += str(i) + " - #" + linkdict[key] + "  ->  "
                # link_list += key + "\n"
                i = i + 1
            return link_list
    return "Not saved links!"


def remove_links(user):
    links = json.load(open('./data/links.json'))

    i = 1
    for majorkey, linkdict in links.items():
        if str(majorkey) == str(user):
            if not bool(links[str(user)]):
                return "Not saved links!"
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
        if len(message.text.split(' ')) == 2:
            url = message.text.split(' ')[1]
            tag = ''
        else:
            url = message.text.split(' ')[1]
            tag = message.text.split(' ')[2]
            save_link(message.chat.id, url, tag)
            bot.reply_to(message, "Link saved!")


@bot.message_handler(commands=['tag'])
def send_save_tag_link(message):
    saveUser(message.chat.id)
    if message.reply_to_message is None or message.reply_to_message.text == "":
        bot.reply_to(message, "You have to reply a message")
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, "You have to specify the tag")
        return
    url = message.reply_to_message.text
    tag = message.text.split()[1]
    save_link(message.chat.id, url, tag)
    bot.reply_to(message, "Link saved!")


@bot.message_handler(func=lambda message: isUserAnswer(message.from_user.id, userTracking))
def catch_save_link(message):
    if len(message.text.split(' ')) == 1:
        url = message.text.split(' ')[0]
        tag = ''
    else:
        url = message.text.split(' ')[0]
        tag = message.text.split(' ')[1]
        save_link(message.chat.id, url, tag)
        del userTracking[message.chat.id]
        bot.reply_to(message, "Link saved!")


@bot.message_handler(commands=['removeall'])
def send_remove_links(message):
    cid = message.chat.id
    saveUser(cid)
    removeMessage = remove_links(cid)
    bot.reply_to(message, removeMessage)

# Root commands


@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")

# Start the bot
bot.polling()
