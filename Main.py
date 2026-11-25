import machine
import time
import Pin

# La broche 2 contrôle souvent la LED bleue intégrée
led = machine.Pin(0, machine.Pin.OUT)

print("Démarrage du clignotement...")

while True:
    led.value(not led.value()) # Inverse l'état de la LED
    time.sleep(0.5)            # Attend 500ms