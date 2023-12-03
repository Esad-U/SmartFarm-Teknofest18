import serial
import time

#Su pompasi
def Pompa():
    usbCom = serial.Serial('/dev/ttyACM0',9600)
    usbCom.open()
    usbCom.write('calistir')
#DHT11
def Read_Temp():
    serTemp = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate = 9600,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        timeout = 1)
    temp = serTemp.readline()
    print(temp)
def Read_Hum():
    serHum = serial.Serial(
            port = '/dev/ttyACM0',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            timeout = 1)
    humid = serHum.readline()
    print(humid)
#Toprak nem
def Read_Hum2():
    serHum2 = serial.Serial(
            port = '/dev/ttyACM0',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            timeout = 1)
    humid2 = serHum2.readline()
    print(humid2)
#Agirlik sensoru
def Read_Weight():
    serWeig = serial.Serial(
            port = '/dev/ttyACM0',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            timeout = 1)
    weight = serWeig.readline()
    print(weight)

while True:
    Read_Temp()