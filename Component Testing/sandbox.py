if button.value() == 1:# code for displaying realtime mositure data on LCD when button is pushed
    lcd.backlight_on()
    lcd.display_on()
    pump.value(1)
    moisturepower.value(1)
    soil =  moisture.read_u16()
    percentage = round(((soil-65535)*100)/(49007-65535),2)
    out_string = "Soil Moisture: " 
    lcd.putstr(out_string)
    lcd.move_to(0,1)
    lcd.putstr(str(percentage) +"%")
    moisturepower.value(0)
    utime.sleep(2)
    lcd.clear()
elif button.value() == 0:# code for turning off LCD display when button is released
    moisturepower.value(0)
    lcd.clear()
    lcd.backlight_off()
    lcd.display_off()
    pump.value(0)
    # bluetooth code
elif uart.any():
    data = uart.read()
    data =  str(data)
    print(data)
    
    if ('send_history' in data):#code for sending moisture levels from the past twelve hours
        print("Received order for historical data")
        historical_data = file.read()
        uart.write(historical_data)
    elif ('SendMoisture' in data):# code for sending moisture data to phone
        print("received order for moisture")
        utime.sleep(2)
        moisturepower.value(1)
        soil =  moisture.read_u16()
        percentage = round(((soil-65535)*100)/(49007-65535),2)
        out_string = "Soil Moisture: "
        uart.write(out_string + str(percentage))
        moisturepower.value(0)
    elif('PumpOn' in data):# code for turning pump on
        print("received pump order")
        pump.value(1)
    elif('PumpOff' in data):# code for turning pump off
        pump.value(0)