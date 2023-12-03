import _thread
from gpiozero import MCP3008
import time
import serial
import dht11
import RPi.GPIO as GPIO
import urllib
import paho.mqtt.client as paho

tarla_API = "RPNVZZF7E3S3XRL0"
diger_API = "Z84JIRALRHZNAWM0"


sen1= MCP3008(channel = 0)
sen2= MCP3008(channel = 1)
sen3= MCP3008(channel = 2)
sen4= MCP3008(channel = 3)
sen5= MCP3008(channel = 4)
sen6= MCP3008(channel = 5)
sen7= MCP3008(channel = 6)
sen8= MCP3008(channel = 7)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
pompa = 21
GPIO.setup(pompa, GPIO.OUT)

instance = dht11.DHT11(pin=2)



def pompa():
    GPIO.output(pompa,GPIO.HIGH)
def pomp():
    GPIO.output(pompa,GPIO.LOW)
def tarla():
    while mesaj == "toprakOn":
        Bolge1 = sen1.value
        Bolge1 = 100 - Bolge1*100
        print("Bolge1",int(Bolge1))
    
        Bolge2 = sen2.value
        Bolge2 = 100 - Bolge2*100
        print("Bolge2",int(Bolge2))
    
        Bolge3 = sen3.value
        Bolge3 = 100 - Bolge3*100
        print("Bolge3",int(Bolge3))    
    
    
        Bolge4 = sen4.value
        Bolge4 = 100 - Bolge4*100
        print("Bolge4",int(Bolge4))
    
        Bolge5 = sen5.value
        Bolge5 = 100 - Bolge5*100
        print("Bolge5",int(Bolge5))
    
        Bolge6 = sen6.value
        Bolge6 = 100 - Bolge6*100
        print("Bolge6",int(Bolge6))
    
        Bolge7 = sen7.value
        Bolge7 = 100 - Bolge7*100
        print("Bolge7",int(Bolge7))
    
        Bolge8 = sen8.value
        Bolge8 = 100 - Bolge8*100
        print("Bolge8",int(Bolge8))
    
        toplam = Bolge1+Bolge2+Bolge3+Bolge4+Bolge5+Bolge6+Bolge7+Bolge8
        global ortalama
        ortalama = toplam/8
        print (int(ortalama))
        if Bolge1 < 30 or Bolge2 < 30 or Bolge3 < 30 or Bolge4 < 30 or Bolge5 < 30 or Bolge6 < 30 or Bolge7 < 30 or Bolge8 < 30:
            pompa()
        else:
            pomp()
    
        istek_tarla = urllib.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}&field7={}&field8={}".format(tarla_API,Bolge1,Bolge2,Bolge3,Bolge4,Bolge5,Bolge6,Bolge7,Bolge8))
        iseter_tarla = urllib.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}".format(diger_API,ortalama))
def Agirlik():
    while mesaj == "agirlikOn":
        ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            timeout = 1)
        global data 
        data = ser.readline()
        print(str(data))#milimetresil
        isteri_tarla = urllib.urlopen("https://api.thingspeak.com/update?api_key={}&field3={}".format(diger_API,data))
    
def sicaklik_ak():
    while mesaj == "dhtOn":
        instance = dht11.DHT11(pin=2)
        result = instance.read()
        global sicaklik
        sicaklik = result.temperature
        print("Temperature: %d C" % sicaklik)
        isterim_tarla = urllib.urlopen("https://api.thingspeak.com/update?api_key={}&field2={}".format(diger_API,sicaklik))

def baglanti_saglandiginda(client, userdata, flags, rc):
	print("Baglandi, rc:" + str(rc))
	client.subscribe("piton/feeds/pitonlar", 0)
def mesaj_geldiginde(client, userdata, msg):
	global mesaj
	mesaj = msg.payload
	if mesaj == "Su Pompasi Acik":
        _thread.start_new_thread(pompa,())
    elif mesaj == "Su Pompasi Kapali":
        _thread.start_new_thread(pomp,())
    elif mesaj == "dhtOn":
        _thread.start_new_thread(sicaklik_ak,())
    elif mesaj == "toprakOn":
        _thread.start_new_thread(tarla,())
    elif mesaj == "agirlikOn":
        _thread.start_new_thread(Agirlik,())

def iletisim():	
    istemci = paho.Client()
    istemci.on_connect = baglanti_saglandiginda
    istemci.on_message = mesaj_geldiginde
    istemci.username_pw_set("piton","d77f7e7719fb43729d521d395749d1e2")
    istemci.connect("io.adafruit.com", port=1883)
    istemci.loop_forever()
try:
    _thread.start_new_thread(iletisim,())
except:
    print("Unable to start thread.")
while 1:
    pass

   #ister_tarla = urllib.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}".format(diger_API,ortalama, sicaklik))
    
    
    
#urlopen(tarla_URL + '&field1=%s&field2=%sfield3=%s&field4=%s&field5=%s&field6=%s&field7=%s&field8=%s&' % Tarlalar[0],Tarlalar[1],Tarlalar[2],Tarlalar[3],Tarlalar[4],Tarlalar[5],Tarlalar[6],Tarlalar[7])
#conn = urllib2.urlopen(diger_URL + '&field1=%s&field2=%sfield3=%s' % ()))

