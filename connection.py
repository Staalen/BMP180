import network, time
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
# kobler til med SSID og passord
sta_if.connect("VG3Data", "Admin:1234") 
# venter til tilkoblingen er etabert
while not sta_if.isconnected():
    time.sleep(0.1)
# printer ip adresse som enheten har fått
print(sta_if.ifconfig())