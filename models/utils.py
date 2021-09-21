import telegram

def send_picture(chat_id,path,token):
  bot = telegram.Bot(token)
  bot.send_photo(chat_id=chat_id,photo=open(path,"rb"))