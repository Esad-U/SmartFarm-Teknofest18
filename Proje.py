import thread
import paho.mqtt.client as paho
from time import sleep
import RPi.GPIO as gpio
import time
import dht11
import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np





gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()

#SERVO MOTORLAR
serv1 = 12
serv2 = 13
serv3 = 19
gpio.setup(serv1, gpio.OUT)
gpio.setup(serv2, gpio.OUT)
gpio.setup(serv3, gpio.OUT)
servo1 = gpio.PWM(serv1, 50)
servo2 = gpio.PWM(serv2, 50)
servo3 = gpio.PWM(serv3, 50)
servo1.start(5)
servo2.start(5)
servo3.start(5)
#HAREKET SENSORU DEGiSKENLER
hareket_pin = 22
buzzer_pin  = 10
gpio.setup(hareket_pin, gpio.IN)
gpio.setup(buzzer_pin, gpio.OUT)

#NEM SENSORLERi
a1 = dht11.DHT11(pin=4)
a2 = dht11.DHT11(pin=3)
veri = a1.read()
veri2 = a2.read()

#MESAFE SENSORU
trig = 21
echo = 20
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

#DC MOTOR
istenilen_sicaklik = 182
istneilen_nem = 24

Motor1A = 23
Motor1B = 24
Motor1E = 25
a3 = dht11.DHT11(pin=2)
gpio.setup(Motor1A,gpio.OUT)
gpio.setup(Motor1B,gpio.OUT)
gpio.setup(Motor1E,gpio.OUT)
def servoDondur(aci,servo):
    servo.ChangeDutyCycle(5+aci/180.0*5)

def servo(mesa, servo):
    while(mesaj == mesa):
        for i in range(180):
            servoDondur(i,servo)
            time.sleep(0.01)
        for i in range(180):
            servoDondur(180-i,servo)
            time.sleep(0.01)
#DHT11LERE GORE TARLA SULAMA KODU
def toprak():
    print('Sicaklik 1:', veri.temperature, 'Nem 1:', veri.humidity)
    print('Sicaklik 2:', veri2.temperature, 'Nem 2:', veri2.humidity)
    if veri.is_valid():
	if veri.humidity < 50 and veri2.humidity >= 50:
            servo(servo1)
        elif veri.humidity >= 50 and veri2.humidity < 50:
            servo(servo2)
            
    else:
        print('Veri hatali!')

    time.sleep(3)

#SU TANKERiNDE NE KADAR SU KALDiGiNi GORMEK iCiN MESAFE SENSORU KODU(DAHA DENENMEDi)
def mesafe():
    gpio.output(trig, False)


    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    while gpio.input(echo)==0:
        pulse_start = time.time()

    while gpio.input(echo)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > 2 and distance < 400:
        print "Mesafe:",distance - 0.5,"cm"
    else:
        print "Menzil asildi"
def a():
    print("MADE BY OLUM PITON")




def sera():
    result = a3.read()
    okunan_sicaklik = result.temperature
    okunan_nem = result.humidity
    if  okunan_sicaklik > istenilen_sicaklik:
        gpio.output(Motor1A,gpio.HiGH)
        gpio.output(Motor1B,gpio.LOW)
        gpio.output(Motor1E,gpio.HiGH)
    else :
        gpio.output(Motor1E,gpio.LOW)

    if result.humidity < 50:
        servo(servo3)


def pir():
     print "t"
     while(mesaj== "pir"):
        if gpio.input(hareket_pin):
            print("HAREKET ALARMi!")
            gpio.output(buzzer_pin, True)
            time.sleep(1.5)
            gpio.output(buzzer_pin, False)
        time.sleep(0.5)
        
def baglanti_saglandiginda(client, userdata, flags, rc):
	print("Baglandi, rc:" + str(rc))
	client.subscribe("piton/feeds/pitonlar", 0)
def mesaj_geldiginde(client, userdata, msg):
	global mesaj
	mesaj = msg.payload
	if mesaj == "pir":
        thread.start_new_thread( pir,())    
    elif mesaj == "mesafe":
        thread.start_new_thread(mesafe,())
    elif mesaj == "kamera":
        thread.start_new_thread(kamera,())
    elif mesaj == "DHT11 toprak":
        thread.start_new_thread(toprak,())
    elif mesaj == "DHT11 sera":
        thread.start_new_thread(sera,())
    elif mesaj == "servo1":
        thread.start_new_thread(servo,(mesaj,servo1))
    elif mesaj == "servo2":
        thread.start_new_thread(servo,(mesaj,servo2))
    elif mesaj == "servo3":
        thread.start_new_thread(servo,(mesaj,servo3))
    #else:
   #    thread.start_new_thread(a,())

def iletisim():	
	istemci = paho.Client()
	istemci.on_connect = baglanti_saglandiginda
	istemci.on_message = mesaj_geldiginde
	istemci.username_pw_set("piton","d77f7e7719fb43729d521d395749d1e2")
	istemci.connect("io.adafruit.com", port=1883)
	istemci.loop_forever()
mesaj="t3"
try:
   thread.start_new_thread( iletisim, ()) 
except:
    print "Error: unable to start thread"
   
while 1:
    pass
