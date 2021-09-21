from models.utils import send_picture
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from models.AudioPlayer import AudioPlayer, TelegramAudio
from models.Camera import Camera
import os

class TelegramBot():
  def __init__(self,token):
      self.token = token
  
  def init(self):
    updater = Updater(self.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start",start))
    dispatcher.add_handler(CommandHandler("picture",take_picture))
    dispatcher.add_handler(CommandHandler("stream",start_stream))
    dispatcher.add_handler(MessageHandler(Filters.attachment, capture_audio))

    updater.start_polling()
    updater.idle()

def start(update,context):
  user = update.effective_user
  update.message.reply_markdown_v2(f'Hi {user.mention_markdown_v2()}\!')

def capture_audio(update,context):
  if(update.message.voice != None):
    audio = TelegramAudio(os.environ['TOKEN'],update.message.voice.file_id)
    audio.create_file()
    
    player = AudioPlayer(audio.get_file_name())
    player.init()

    os.remove(audio.get_file_name())
  else:
    print('No telegram audio detected')

def take_picture(update,context):
  camera = Camera('pictures/photo_')
  camera.init_camera()
  path = camera.take_picture()
  send_picture(update.message.chat.id,path,os.environ['TOKEN'])

def start_stream(update,context):
  camera = Camera('pictures/photo_')
  camera.init_camera()
  camera.start_stream()
