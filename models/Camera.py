import cv2
from datetime import datetime

class Camera():
  def __init__(self,path,window_name='camera',camera_index=0):
    self.name = window_name
    self.index = camera_index
    self.path = path
    self.capture = None

  def init_camera(self):
    capture = cv2.VideoCapture(self.index)
    if not capture.isOpened():
      raise RuntimeError('Check if the camera is on or select another index.')
    else:
      self.capture = capture

  def start_stream(self):
    print('===============================================')
    print('Press q to close camera')
    print(f'Or ress s to save a picture in /pictures')

    while self.capture.isOpened():        
      catch, frame = self.capture.read()
      cv2.imshow(self.name, frame)
      key = cv2.waitKey(10)

      if key == ord('q') or cv2.getWindowProperty(self.name, cv2.WND_PROP_AUTOSIZE) < 1:
        self.close_camera()
      
      if key == ord('s'):
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        cv2.imwrite(f'{self.path}{now}.jpg',frame)

  def take_picture(self):
    catch, frame = self.capture.read()
    now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
    path = f'{self.path}{now}.jpg'
    cv2.imwrite(path,frame)
    return path

  def close_camera(self):
    self.capture.release()
    cv2.destroyAllWindows()
    print('Camera close')
  