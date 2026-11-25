from machine import Pin, I2C, ADC, PWM
from time import sleep, ticks_ms
import random

MAX_DUTY = 1023 

led = PWM(Pin(Pin.board.A7, Pin.OUT))

btn = Pin(Pin.board.A6)

adc = ADC(Pin(Pin.board.A3))
adc.atten(ADC.ATTN_11DB)  

i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70  

i2c.writeto(adresse_matrice, bytes([0x21])) 
i2c.writeto(adresse_matrice, bytes([0x81]))
i2c.writeto(adresse_matrice, bytes([0xE4])) 



def defineMap(matrice):
    for row in range(0, 16, 2):
            map = 1 << random.randrange(0, 7)
            matrice.writeto(adresse_matrice, bytes([row, map])) 

def set_white_brightness(brightness):
    led.duty(int(min(MAX_DUTY, max(0, brightness * MAX_DUTY))))


def fermeTout(matrice):
    for row in range(0, 16, 2):
        matrice.writeto(adresse_matrice, bytes([row, 0]))

def allumeTout(matrice):
    for row in range(0, 16, 2):
        matrice.writeto(adresse_matrice, bytes([row, 0b11111111]))

fermeTout(i2c)


def afficherLettre(matrice, lettre, lettreMapping):
    mapping = lettreMapping[lettre]
    index = 0
    for row in [10, 8, 6, 4, 2]:
        matrice.writeto(adresse_matrice, bytes([row, mapping[index] << 2]))
        index += 1


mappingSecret = defineMap
index_lum_actuelle = 0
MAX_VALUE_ADC = 4095

print("\033[2J\033[H", end="") 
print("=== JEU : TROUVE LA CLÉ ===")
print("Tournez le potentiometre pour choisir la lumière a allumer .")
print("clicker sur le bouton pour valider.")

flash_toggle = False

cur_btn_state = btn.value()
last_btn_state = cur_btn_state

fermeTout(i2c)
lastFlash = ticks_ms()
try:
    while index_lumière < len():
        cur_btn_state = btn.value()

        led.duty(int(max(0, min(MAX_DUTY, MAX_DUTY * (1- distLum / 26)))))

        if cur_btn_state != last_btn_state and cur_btn_state == 0:
            if distLum == 0:
                index_lum_actuelle += 1
                print("\033[2J\033[H", end="") 
                print("=== JEU : TROUVE LE MOT ===")
                print(f"Felicitation, vous avez trouvé une partie de la clé")
            else:
                print("\033[2J\033[H", end="") 
                print("=== JEU : TROUVE LE MOT ===")
                print(f"Dommage, cettte lumière ne fait pas parti de la clé")
        last_btn_state = cur_btn_state
        sleep(0.05)
    print("\033[2J\033[H", end="") 
    print(f"Felicitation, vous avez trouver la clé")
except KeyboardInterrupt:
    led.duty(0)
    led.deinit()

    fermeTout(i2c)