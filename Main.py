from machine import Pin, I2C, ADC, PWM
from time import sleep, ticks_ms
import random

MAX_DUTY = 1023 

led_r = PWM(Pin(Pin.board.A1, Pin.OUT))
led_g = PWM(Pin(Pin.board.A3, Pin.OUT))
led_b = PWM(Pin(Pin.board.A3, Pin.OUT))

cursor_x = A6
cursor_y = A7
cursor_btn = D2

i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70  

i2c.writeto(adresse_matrice, bytes([0x21])) 
i2c.writeto(adresse_matrice, bytes([0x81]))
i2c.writeto(adresse_matrice, bytes([0xE4])) 



def defineMap(matrice):
    nouvelle_map = []

    for row in range(0, 16, 2):
        led_position = random.randrange(0, 8)
        valeur = 1 << led_position

        matrice.writeto(adresse_matrice, bytes([row, valeur]))
        nouvelle_map.append(led_position)
    return nouvelle_map


def set_white_brightness(brightness):
    led.duty(int(min(MAX_DUTY, max(0, brightness * MAX_DUTY))))


def fermeTout(matrice):
    for row in range(0, 16, 2):
        matrice.writeto(adresse_matrice, bytes([row, 0]))

def allumeTout(matrice):
    for row in range(0, 16, 2):
        matrice.writeto(adresse_matrice, bytes([row, 0b11111111]))

def afficherCurseur(matrice, x, y):
    fermeTout(matrice)

    valeur = 1 << x
    matrice.writeto(adresse_matrice, bytes([y * 2, valeur]))

def afficherMap(matrice, map_led):
    for y in range(8):
        matrice.writeto(
            adresse_matrice,
            bytes([y * 2, map_led[y]])
        )
fermeTout(i2c)


mappingSecret = defineMap(i2c)
print(mappingSecret)
index_lum_actuelle = 0
MAX_VALUE_ADC = 4095

print("\033[2J\033[H", end="") 
print("=== JEU : TROUVE LA CLÉ ===")
print("Tournez le potentiometre pour choisir la lumière a allumer .")
print("clicker sur le bouton pour valider.")

flash_toggle = False
cursor_x = 0
cursor_y = 0

cur_btn_state = btn.value()
last_btn_state = cur_btn_state

fermeTout(i2c)
lastFlash = ticks_ms()
try:
    while currentMapping != mappingSecret:

        if joystick_droite:
            cursor_x = min(7, cursor_x + 1)

        elif joystick_gauche:
            cursor_x = max(0, cursor_x - 1)

        elif joystick_haut:
            cursor_y = max(0, cursor_y - 1)

        elif joystick_bas:
            cursor_y = min(7, cursor_y + 1)

        afficherCurseur(i2c, cursor_x, cursor_y)

        cur_btn_state = btn.value()
        led.duty(int(max(0, min(MAX_DUTY, MAX_DUTY * (1- distLum / 26)))))



        if cur_btn_state != last_btn_state and cur_btn_state == 0:
            
            if cursor_x == cle_secreteprint("Bonne LED!")
                index_lum_actuelle += 1
                print("\033[2J\033[H", end="") 
                print(f"Felicitation, vous avez trouvé une partie de la clé")
            else:
                print("\033[2J\033[H", end="")
                print(f"Dommage, cettte lumière ne fait pas parti de la clé")

        last_btn_state = cur_btn_state
        sleep(0.05)
    print("\033[2J\033[H", end="") 
    print(f"Felicitation, vous avez trouver la clé")
except KeyboardInterrupt:
    led.duty(0)
    led.deinit()

    fermeTout(i2c)