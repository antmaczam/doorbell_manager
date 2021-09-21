import pyglet,urllib.request,json

class AudioPlayer():
  def __init__(self,file_name,local_files=True,interval_update=1):
    self.file_name = file_name
    self.music_duration = 0
    self.dt_ac = 0
    self.local_files = local_files
    self.interval_update = interval_update

  def init(self):
    pyglet.options['search_local_libs'] = self.local_files
    pyglet.clock.schedule_interval(self.update,self.interval_update)

    my_music = pyglet.media.load(self.file_name)
    self.music_duration = my_music.duration
    my_player = pyglet.media.Player()

    my_player.queue(my_music)	
    my_player.play()
    pyglet.app.run()    

  def update(self,dt):
    if self.dt_ac > self.music_duration:
      pyglet.app.exit()
    else:
      self.dt_ac += dt

class TelegramAudio():
  def __init__(self,bot_token,file_id):
    self.bot_token = bot_token
    self.file_id = file_id
    self.file_name = None
  
  def get_file_name(self):
    return self.file_name
    
  def get_path(self):
    url = f'https://api.telegram.org/bot{self.bot_token}/getFile?file_id={self.file_id}'
    request = urllib.request.urlopen(url)
    return json.loads(request.read())['result']['file_path']  

  def get_file(self,file_path):
    url = f'https://api.telegram.org/file/bot{self.bot_token}/{file_path}'
    request = urllib.request.urlopen(url)
    return request.read()

  def write_file(self,data,file_name,mode='wb'):
    self.file_name = file_name
    f = open(file_name,mode)
    f.write(data)

  def create_file(self):
    try:
      path = self.get_path()
      file_data = self.get_file(path)
      self.write_file(file_data,path[6:])
    except Exception:
      print('The path can not request, do you have internet connection?')