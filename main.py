import _thread
import time
import game
import led_multiplex
from collections import namedtuple
from ssd1306 import SSD1306_I2C
from machine import I2C
from machine import Pin, PWM


i2c = I2C(0, sda=Pin(0), scl=Pin(1))
oled = SSD1306_I2C(128, 64, i2c)

rows = [Pin(i, Pin.OUT) for i in [19, 18, 17, 16]]
cols = [Pin(i, Pin.OUT) for i in [12, 13, 14, 15]]
leds = led_multiplex.LedMultiplex(rows, cols, 1, 90)

gamebuttons = namedtuple('GameButtons', ['start', 'stop'])
buttons = gamebuttons(start=Pin(2, Pin.IN, Pin.PULL_UP), stop=Pin(3, Pin.IN, Pin.PULL_UP))


oled.fill(1)
oled.text('READY!', 42, 36, 0)
oled.show()
while True:
    game_ = game.Game(leds, oled, buttons)
    game_.play(rounds=10)
