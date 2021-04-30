from pyfirmata import Arduino, ArduinoMega
from pyfirmata import util
from urllib.request import urlopen
from sense_hat import SenseHat

from twilio.rest import Client

from time import *

WRITE_API_KEY='84WCC2MEXXXWG05E'

baseURL='https://api.thingspeak.com/update?api_key=84WCC2MEXXXWG05E&field1=0'

sense = SenseHat()
sense.clear()
red = (255,0,0)

def setBoard(boardType, port):
  if boardType == 'arduino':
    board = Arduino(port)
  else:
    board = ArduinoMega(port)
  return board
board=setBoard('arduino', '/dev/ttyACM0')
reader = util.Iterator(board)
reader.start()

twilio_account = 'ACc6cc91a2e1c216cf6b76b0be4226a37a'
twilio_token = '8e775127852d490db43b7cd93f14a6b4'

pin_var = board.get_pin('d:13:i')


twilio_client = Client(twilio_account, twilio_token)

def writeData(motion):
    conn = urlopen(baseURL + '&field1=%s' % (motion))
    print(conn.read())
    conn.close()

while True:
  if pin_var.read():
    message =twilio_client.messages.create(to='+353 838891787', from_='+14693363435', body='Motion has been detected in your room')
    sense.show_message("MOTION DETECTED!", text_colour = red)
    print('motion detected')
    sleep (180)
    writeData(1)

  else:
    print('No Motion Detected')
    sleep (60)
    writeData(0)