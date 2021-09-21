import telegram
from models.Camera import Camera

DEFAULT_PATH = 'pictures/photo_'

def send_picture(update_object,path,token):
  bot = telegram.Bot(token)
  if(update_object.message != None):
    bot.send_photo(chat_id=update_object.message.chat.id,photo=open(path,"rb"))
  else:
    bot.send_photo(chat_id=update_object.callback_query.message.chat.id,photo=open(path,"rb"))

def take_picture(path=DEFAULT_PATH):
  camera = Camera(path)
  camera.init_camera()
  return camera.take_picture()

def capture_doorbell():
  print("Try capturing some signals from RPi!")