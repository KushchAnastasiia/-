import smbus
import datetime
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
bus = smbus.SMBus(1)
address = 0x29
arr = [7,8,18,16,15,13,12,11]

bus.write_byte(address, 0xa0)
bus.write_byte(address, 0x03)
time.sleep(3)

max_value = 800
light_count = 8
    
while True: 
    bus.write_byte(address, 0xac)
    a = bus.read_byte(address)
    bus.write_byte(address, 0xad)
    b = bus.read_byte(address)
    c = a + b*256
    
    current_lights = 0
    
    if c > max_value:
        current_lights = 8
    else:
        current_lights = c // int(max_value / light_count)
    
    print(c)
    
    for i in arr:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, False)
    
    for i in range(current_lights):
        GPIO.setup(arr[i], GPIO.OUT)
        GPIO.output(arr[i], True)
    
    
    with open('logs/check_lightning.log', 'a+') as file:
        file.write(datetime.datetime.now().isoformat() + ' ' + str(c) + '\n')

    time.sleep(0.5) 