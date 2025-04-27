from machine import Pin
import time
import _thread

# Definición de pines para las bobinas del motor
motor_pins = (12,14,27,26)
bobinas = list()
for i in range(4):
    bobinas.append(Pin(motor_pins[i], Pin.OUT))

led = Pin(2, Pin.OUT)

# Secuencia del motor paso a paso
pasos =(int('C',16), int('6',16),int('3',16),int('9',16)) 

# Variables globales
i = 0  # Puntero del vector
der = False
izq = False
contador_pasos = 0
giros = 0.0
lock = _thread.allocate_lock()

def sacar_datos(datos):
    for i in range(4):
        bit = (datos>>i) & 0x01
        bobinas[i].value(bit)


def motor_paso_der():
    global i, der, contador_pasos, giros
    while True:
        if der:
            lock.acquire()
            i += 1
            if i == 4:
                i = 0
            contador_pasos += 1
            sacar_datos(pasos[i])
            if (contador_pasos%64 == 0):
                giros = contador_pasos/ (64*8)
                print(f"Giro derecha {giros}")
            lock.release()
            time.sleep(0.01)

def motor_paso_izq():
    global i, izq, contador_pasos, giros
    while True:
        if izq:
            lock.acquire()
            i -= 1
            if i == -1:
                i = 3
            sacar_datos(pasos[i])
            contador_pasos -= 1
            if (contador_pasos%64 == 0):
                giros = contador_pasos/ (64*8)
                print(f"Giro Izquierda {giros}")
            lock.release()
            time.sleep(0.01)

def recibir_datos():
    global der, izq
    while True:
        c = input("Ingrese comando: ")
        if c == 'a':
            der = True
            izq = False
        elif c == 'b':
            der = False
            izq = True
        elif c == 'c':
            der = False
            izq = False
        else:
            der = False
            izq = False
        time.sleep(0.1)


sacar_datos(10)
time.sleep(3)
# Inicio de hilos
_thread.start_new_thread(motor_paso_der, ())
_thread.start_new_thread(motor_paso_izq, ())
_thread.start_new_thread(recibir_datos, ())

print("Arranque...")
while True:
    led = 1
    time.sleep(0.5)
    led = 0
    time.sleep(0.5)
    