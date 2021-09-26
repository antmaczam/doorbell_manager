from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from models.AudioPlayer import AudioPlayer, TelegramAudio
import os

from models.utils import Camera, send_picture, take_picture, DEFAULT_PATH

class TelegramBot():
  def __init__(self,token):
      self.token = token
  
  def init(self):
    updater = Updater(self.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("comenzar",start))
    dispatcher.add_handler(CommandHandler("foto",take_picture))
    dispatcher.add_handler(CommandHandler("video",start_stream))
    dispatcher.add_handler(CommandHandler("abrir",open_door))
    dispatcher.add_handler(MessageHandler(Filters.attachment, capture_audio))

    updater.start_polling()
    updater.idle()

def start(update,context):
  keyboard = [['/foto', '/video'],['/abrir']]
  msg = '¡Comencemos! A continuación aparecerá la lista de comandos disponibles'
  reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)
  update.message.reply_text(text=msg,reply_markup=reply_markup)

def take_picture(update,context):
  camera = Camera(DEFAULT_PATH)
  camera.init_camera()
  picture_name = camera.take_picture()
  send_picture(update,picture_name,os.environ['TOKEN'])

def start_stream(update,context):
  camera = Camera(DEFAULT_PATH)
  camera.init_camera()
  camera.start_stream()

def capture_audio(update,context):
  if(update.message.voice != None):
    audio = TelegramAudio(os.environ['TOKEN'],update.message.voice.file_id)
    audio.create_file()
    
    player = AudioPlayer(audio.get_file_name())
    player.init()

    os.remove(audio.get_file_name())
  else:
    print('No telegram audio detected')

def open_door(update,context):
  print('Sending signal to open de door!')