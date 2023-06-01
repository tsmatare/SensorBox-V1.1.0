import machine
import utime

moisture = machine.ADC(26)
moto = machine.Pin(15,machine.Pin.OUT)

dfuiconversion_factor = 3.3 / (65535)
file = open("huney.txt","w")

try:
    for i in range(1):
        moto.value(1)
        utime.sleep(2)
        soil = moisture.read_u16()
        print(soil)
        file.write(str(soil) +"\n")
        file.flush()
        moto.value(0)
        utime.sleep(9)
        
    for i in range(10):
        moto.value(1)
        utime.sleep(2)
        soil = moisture.read_u16()
        percentage = round(((soil-63837.25)*100)/(27000-63837.25),2)
        print(str(percentage) +"%")
        moto.value(0)
        utime.sleep(1)
        
except KeyboardInterrupt:
    print("bye")
