from machine import Pin, PWM
import utime
import random

#RGB LED
red_led = PWM(Pin(5))
green_led = PWM(Pin(4))
blue_led = PWM(Pin(3))

#BUTTONS
button_red = Pin(12, Pin.IN, Pin.PULL_UP)   
button_green = Pin(13, Pin.IN, Pin.PULL_UP)
button_yellow = Pin(14, Pin.IN, Pin.PULL_UP)
button_blue = Pin(11, Pin.IN, Pin.PULL_UP)

#LISTS
colors = ['red', 'green', 'blue', 'yellow']
game = []

score = 0

# set LED color
def set_color(r, g, b, delay):
    scale = 0.05  # Reduce brightness
    max_brightness = 65535  
    min_brightness = int(max_brightness * scale)

    red_duty = int(max_brightness - (r * min_brightness / 255))
    green_duty = int(max_brightness - (g * min_brightness / 255))
    blue_duty = int(max_brightness - (b * min_brightness / 255))

    # Apply the duty values to the LEDs
    red_led.duty_u16(red_duty)
    green_led.duty_u16(green_duty)
    blue_led.duty_u16(blue_duty)
    utime.sleep(delay)


# Initialize LEDs
red_led.freq(1000)
green_led.freq(1000)
blue_led.freq(1000)



def add_color():
    game.append(random.choice(colors))

def game_over():
    set_color(255, 0, 0, 1)
    global stop_game
    stop_game = True
    print(game)
    print("Score = ", score)

def button_pressed():
    if not button_red.value():
        return 'red'
    if not button_green.value():
        return 'green'
    if not button_yellow.value():
        return 'yellow'
    if not button_blue.value():
        return 'blue'

def play_colors():
    for x in game :
        if x=='red' :
            set_color(255, 0, 0, 1) # Red
            set_color(0, 0, 0, 1)
        elif x=='green' :
            set_color(0, 255, 0, 1) # Green*
            set_color(0, 0, 0, 1)
        elif x=='blue' :
            set_color(0, 0, 255, 1) # Blue
            set_color(0, 0, 0, 1)
        elif x=='yellow' :
            set_color(255, 150, 0, 1) # Yellow
            set_color(0, 0, 0, 1)

    

def player_turn():
    for color in game:
        pressed = None
        print(color)
        utime.sleep(0.5)
        while pressed is None:
            pressed = button_pressed()
        if pressed != color:
            return game_over()
 
    set_color(255, 255, 255, 1) # white for win
    global score
    score += 1 
    utime.sleep(3)

stop_game = False
#Start game
while stop_game!=True :
    add_color()
    play_colors()
    #print(game)
    player_turn()
    

    