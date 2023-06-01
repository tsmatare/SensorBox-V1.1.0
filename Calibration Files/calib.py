import machine
import utime

moisture = machine.ADC(26)
moto = machine.Pin(15,machine.Pin.OUT)

conversion_factor = 3.3 / (65535)

for i in range(64):
    moto.value(1)
    utime.sleep(2)
    soil = moisture.read_u16()
    percentage = round(((soil-65535)*100)/(49007-65535),2)
    print(percentage)
    file.write(str(soil) +"\n")
    file.flush()
    utime.sleep(1)