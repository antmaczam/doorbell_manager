import telegram
from models.Camera import Camera
import os
import requests
import RPi.GPIO as GPIO
import time

DEFAULT_PATH = 'pictures/photo_'
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def send_picture(chat_id,path,token):
  bot = telegram.Bot(token)
  bot.send_photo(chat_id=chat_id,photo=open(path,"rb"))

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
  
def listen_to_rpi():
  try:
    print("Config rpi pins")
    pin = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.IN)
    while True:
      push_pin = GPIO.input(pin)
      if push_pin == 1:
        capture_doorbell()
        send_picture(CHAT_ID,take_picture(),TOKEN)
        time.sleep(3)
  except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO clean up")
    #updater.idle()
    #print("\nBot stoped")

def send_signal_open_door():
  pin = 13
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,True)
  time.sleep(3)
  GPIO.output(pin,False)
