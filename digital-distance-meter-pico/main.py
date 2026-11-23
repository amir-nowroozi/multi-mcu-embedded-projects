from machine import Pin, I2C
from time import sleep
from vl53l0x import VL53L0X
from ssd1306 import SSD1306_I2C


# --------------------------------
# I2C configuration
# --------------------------------

i2c_sensor = I2C(
    1,
    sda=Pin(2),
    scl=Pin(3)
)

i2c_oled = I2C(
    0,
    sda=Pin(8),
    scl=Pin(9)
)


# --------------------------------
# Button and LEDs
# --------------------------------

button = Pin(28, Pin.IN, Pin.PULL_UP)

led_green = Pin(17, Pin.OUT)
led_orange = Pin(18, Pin.OUT)
led_red = Pin(20, Pin.OUT)

led_green.off()
led_orange.off()
led_red.off()


# --------------------------------
# Check connected I2C devices
# --------------------------------

print("VL53L0X I2C devices:", i2c_sensor.scan())
print("OLED I2C devices:", i2c_oled.scan())


# --------------------------------
# Initialize sensor and OLED
# --------------------------------

sensor = VL53L0X(i2c_sensor)
oled = SSD1306_I2C(128, 64, i2c_oled)


def oled_clear():
    oled.fill(0)
    oled.show()


def oled_write(text, x, y):
    oled.text(str(text), x, y)
    oled.show()


def turn_off_leds():
    led_green.off()
    led_orange.off()
    led_red.off()


def check_leds(distance):
    if distance > 200:
        led_green.on()
        led_orange.off()
        led_red.off()

    elif distance > 100:
        led_green.off()
        led_orange.on()
        led_red.off()

    else:
        led_green.off()
        led_orange.off()
        led_red.on()


oled_clear()
oled.text("VL53L0X", 25, 10)
oled.text("Starting...", 20, 30)
oled.show()

sleep(1)


# --------------------------------
# Variables
# --------------------------------

menu_number = 1

min_distance = 9999
max_distance = 0

old_button_value = 1


# --------------------------------
# Main program
# --------------------------------

try:
    sensor.start()

    while True:
        
        total = 0
        count = 10
        
        for i in range(count):
            distance = sensor.read()
            distance -= 50
            
            if distance < 0 :
                distance = 0
                
            total = total + distance
            sleep(0.01)
            
        avg_distance = total / count 
            

        print("Distance:", int(avg_distance), "mm")

        # ذخیره کمترین فاصله
        if avg_distance < min_distance:
            min_distance = avg_distance

        # ذخیره بیشترین فاصله
        if avg_distance > max_distance:
            max_distance = avg_distance

        # روشن کردن LEDها
        check_leds(avg_distance)

        # خواندن وضعیت دکمه
        button_value = button.value()

        # اگر دکمه تازه فشار داده شد
        if old_button_value == 1 and button_value == 0:
            if menu_number == 1:
                menu_number = 2
            else:
                menu_number = 1

            sleep(0.25)

        old_button_value = button_value

        # نمایش منوی شماره 1
        if menu_number == 1:
            oled.fill(0)
            oled.text("Menu 1", 0, 0)
            oled.text("Live Distance", 0, 15)
            oled.text("{} mm".format(int(avg_distance)), 0, 35)

            if avg_distance <= 100:
                oled.text("DANGER!", 0, 55)
            elif avg_distance <= 200:
                oled.text("WARNING", 0, 55)
            else:
                oled.text("SAFE", 0, 55)

            oled.show()

        # نمایش منوی شماره 2
        if menu_number == 2:
            oled.fill(0)
            oled.text("Menu 2", 0, 0)
            oled.text("Min and Max", 0, 15)
            oled.text("Min: {} mm".format(int(min_distance)), 0, 35)
            oled.text("Max: {} mm".format(int(max_distance)), 0, 50)
            oled.show()

        sleep(0.1)

except Exception as e:
    print("Sensor error:", e)

    oled.fill(0)
    oled.text("Sensor Error!", 5, 20)
    oled.text(str(e), 0, 40)
    oled.show()

except KeyboardInterrupt:
    print("Program stopped.")

    oled.fill(0)
    oled.text("Stopped!", 30, 25)
    oled.show()

finally:
    sensor.stop()

    turn_off_leds()
