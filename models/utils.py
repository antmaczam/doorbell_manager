import telegram
from models.Camera import Camera
import os
import requests

DEFAULT_PATH = 'pictures/photo_'
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def send_picture(update_object,path,token):
  bot = telegram.Bot(token)
  bot.send_photo(chat_id=update_object.message.chat.id,photo=open(path,"rb"))

def take_picture(path=DEFAULT_PATH):
  camera = Camera(path)
  camera.init_camera()
  return camera.take_picture()

def capture_doorbell():
  send_message('TIMBRE' + u'🔔')
  print("Try capturing some signals from RPi!")

def send_message(message):
  url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=Markdown&text={message}'
  requests.get(url)