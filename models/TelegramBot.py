from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from models.AudioPlayer import AudioPlayer, TelegramAudio
import os

from models.utils import Camera, send_picture, take_picture, DEFAULT_PATH

class TelegramBot():
  def __init__(self,token):
      self.token = token
  
  def init(self):
    updater = Updater(self.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start",start))
    dispatcher.add_handler(CommandHandler("actions",actions))
    dispatcher.add_handler(MessageHandler(Filters.attachment, capture_audio))
    dispatcher.add_handler(CallbackQueryHandler(pattern="picture",callback=take_picture))
    dispatcher.add_handler(CallbackQueryHandler(pattern="stream",callback=start_stream))

    updater.start_polling()
    updater.idle()

def start(update,context):
  user = update.effective_user
  update.message.reply_markdown_v2(f'Hi {user.mention_markdown_v2()}\!')

def actions(update,context):
  button1 = InlineKeyboardButton(text='Stream',callback_data="stream")
  button2 = InlineKeyboardButton(text='Tomar foto',callback_data="picture")
  update.message.reply_text(
      text='Elige una opción',
      reply_markup=InlineKeyboardMarkup([
          [button1,button2]
      ])
  )

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
