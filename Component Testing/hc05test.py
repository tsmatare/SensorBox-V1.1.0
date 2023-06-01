import machine
import utime

tx= machine.Pin(4)
rx = machine.Pin(5)
id = 1
uart= machine.UART(id=id,baudrate=9600,tx=tx,rx=rx)

led= machine.Pin(13,machine.Pin.OUT)

while True:
    if uart.any():
        data= uart.read()
        data = str(data)
        print(data)
        led.value(0)
        
        if('send' in data):
            led.value(1)
        elif ('LED_OFF' in data):
            led.value(0)

