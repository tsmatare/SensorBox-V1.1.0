# importing libraries
import uasyncio as asyncio
import utime
import machine
import _thread
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# configuring LCD settings
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# defining gpio variables
moisture = machine.ADC(26)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
moisturepower = machine.Pin(15,machine.Pin.OUT)
pump = machine.Pin(13,machine.Pin.OUT)
conversion_factor = 3.3 / (65535)

#setting up UART
tx= machine.Pin(4)
rx = machine.Pin(5)
id = 1
uart= machine.UART(id=id,baudrate=9600,tx=tx,rx=rx)

#turning off the LCD 
lcd.backlight_off()
lcd.display_off()

#switching off relays
pump.value(0)

# creating and opening the log file
file = open("log.csv", "w")
hourr = 216000

global loglist
loglist= ["0"]#creating log list

global percentage

def measurement():
    global percentage
    moisturepower.value(1)
    utime.sleep(2)
    soil =  moisture.read_u16()
    percentage = round(((soil-63837.25)*100)/(27000-63837.25),2)
    moisturepower.value(0)
    return percentage

#def addtolist():
#    global loglist
 #   if len(loglist) >= 12:
  #      global loglist
   #     loglist.pop(0)
    #    havana = str(percentage)
     #   loglist.append(havana)
    #else:
     #   global loglist
      #  loglist.append(havana)

async def print_zero():
    while True:
        await asyncio.sleep(1)
        if button.value() == 1:# code for displaying realtime mositure data on LCD when button is pushed
            lcd.backlight_on()
            lcd.display_on()
            lcd.putstr("measuring...")
            percentage = measurement()
            out_string = "Soil Moisture: "
            lcd.clear()
            lcd.putstr(out_string)
            lcd.move_to(0,1)
            lcd.putstr(str(percentage) +"%")
            utime.sleep(5)
            lcd.clear()
            # code for turning off LCD display when button is released
            lcd.backlight_off()
            lcd.display_off()
            # bluetooth code
        elif uart.any():
            data = uart.read()
            data =  str(data)
            print(data)
            
            if ('send_history' in data):#code for sending moisture levels from the past twelve hours
                print("Received order for historical data")
                historical_data =",".join(loglist)
                uart.write(historical_data)
            elif ('SendMoisture' in data):# code for sending moisture data to phone
                print("received order for moisture")
                percentage = measurement()
                uart.write(out_string + str(percentage))
                moisturepower.value(0)
            elif('PumpOn' in data):# code for turning pump on
                print("received pump order")
                pump.value(1)
            elif('PumpOff' in data):# code for turning pump off
                pump.value(0)

# code for logging data every hour
async def print_one():
    while True:
        await asyncio.sleep(30)
        moisturepower.value(1)
        percentage = measurement()
        out_string = "Soil Moisture: " 
        file.write(str(percentage) +",")
        file.flush
        lekod()
        if percentage < 65:
            while True:
                pump.value(1)
                percentage = measurement()
                if percentage > 65:
                    pump.value(0)
                    break          
        moisturepower.value(0)
        print("recorded")

def lekod():
    global loglist
    global percentage
    if len(loglist) >= 12:
        global percentage
        global loglist
        loglist.pop(0)
        havana = str(percentage)
        loglist.append(havana)
    else:
        global percentage
        global loglist
        havana = str(percentage)
        loglist.append(havana)
        print(loglist)
    
async def main():
    await asyncio.gather(print_zero(), print_one())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("bye")

