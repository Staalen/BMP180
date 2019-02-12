import usocket as socket    "Importerer bibliotek"
from bmp180 import BMP180
from machine import I2C, Pin

i2c = I2C(scl=Pin(22),sda=Pin(21), freq=10000)    "Setter opp variabler"
bmp180 = BMP180(i2c)

def read_sensor():    "Definerer 'read_sensor'"
  global temp, temp_percentage, pressure, temps, pressure_percentage    "Setter globale variabler"
  temp = temp_percentage = pressure = pressure_percentage = 0
  try:
    temp = bmp180.temperature
    temp_percentage = (temp+6)/(40+6)*(100)   "Gjør om temperatur til en prosent verdi"
    pressure = int(bmp180.pressure/100)
    pressure_percentage = (pressure/2000)*(100)   "Gjør om trykk til en prosent verdi"
    temps = '{:.1f}'.format(temp)   "Setter max en desimal"

    return(temps)

  except OSError as e:
    return('Failed to read sensor.')

def index():
  header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
  raw_html = open("index.html", "rt")   "Opner 'html.index' og leser av filen"
  html = raw_html.read().format(temp_percentage=temp_percentage, temps=temps, pressure_percentage=pressure_percentage, pressure=pressure)
  return html             "^Kombinerer variabler sammen mellom python og html^"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  read_sensor()
  response = index()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()