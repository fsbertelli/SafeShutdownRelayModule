import RPi.GPIO as GPIO
from time import sleep
import socket
import json

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23


def desligaMaster():

    with open("/home/solarbot/devices.json") as jf:
        config = json.load(jf)
    for inv in config:
        hostname = inv["hostname"]
        host = inv["host"]
        port = inv["port"]
        try:
    
    #HOST = '172.16.1.131'  
    #PORT = 9009     


            print("[!] Conectado: " + inv["hostname"] + " " + inv["host"])
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dest = (inv["host"], inv["port"])

            msg = ('batata')
            while msg != '\x18':
                print("[!] Enviando comando...") 
                udp.sendto (msg.encode(), dest) 
                udp.close()  
                sleep(2)
                         

        except socket.error as e:
                print ("[!] Erro ao conectar: %s" % e) 
                                
        finally:
                udp.close()
def desligaRasp():
    import subprocess
    comando = "/usr/bin/sudo shutdown -h now "
    processo = subprocess.Popen(comando.split(), stdout=subprocess.PIPE)
    sleep(2)
    output = processo.communicate()[0]
    print(output)
try:
    while True:
        button_state = GPIO.input(18)
        if button_state == True:
            print('[!] Desligando devices...')
            desligaMaster()
            sleep(0.5)
            GPIO.cleanup()
            sleep(1)
            print('[!] Desligando PU')
            desligaRasp()    
except:
    GPIO.cleanup()