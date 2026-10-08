from machine import Pin, reset  # Importa reset para reiniciar la Pico
import time
import random
import _thread

# Configuración de pines
pinData = Pin(2, Pin.OUT)
pinLatch = Pin(3, Pin.OUT)
pinClock = Pin(4, Pin.OUT)

# Mensajes y configuración
tiempo = 100
game = [24, 0, 0, 0, 0, 0, 0, 24]
running = True  # Variable para controlar la ejecución de los hilos
#Mensajes
msg = 62
mensaje = [
    0, 0, 0, 0, 0, 0, 0, 0,
    252, 254, 3, 1, 3, 254, 252, 0,# U
    114, 251, 219, 219, 219, 219, 78, 0,# S
    255, 255, 216, 216, 216, 216,# F
    0, 31, 63, 108, 204, 108, 63, 31, 0, 0,# A
    255, 255, 216, 216, 248, 112,# P
    0, 126, 255, 129, 129, 255, 126,# O
    0, 255, 255, 224, 112, 28, 7, 255, 255,# N
    0, 126, 255, 195, 195, 219, 223, 206, 0, 0, 0, 0, 0, 0, 0, 0 # G
    ]
timpoMsgWin = 20
msgp2 = 40
mensajeP2 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    255, 255, 216, 216, 248, 112, 0,    # P
    0, 78, 223, 145, 145, 243, 98, 0, 0,      # 2
    252, 127, 3, 12, 12, 3, 127, 252,
    0, 126, 255, 129, 129, 255, 126,     # O
    0, 255, 255, 224, 112, 28, 7, 255, 255, # N
    0, 0, 0, 0, 0, 0, 0, 0      # 0
    ]
msgp1 = 38
mensajeP1 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    255, 255, 216, 216, 248, 112, 0,    # P
    0, 195, 255, 255, 195, 0, 0,   # I
    252, 127, 3, 12, 12, 3, 127, 252,	#w
    0, 126, 255, 129, 129, 255, 126,     # O
    0, 255, 255, 224, 112, 28, 7, 255, 255, # N
    0, 0, 0, 0, 0, 0, 0, 0      # 0
    ]
def p2_win():
    """Refresca la matriz de LEDs."""
    for y in range(msgp2 + 8):           # Recorrido de tabla
        for p in range(timpoMsgWin):        # Refresco de matriz
            for n in range(8):
                H595(~mensajeP2[n + y], 1 << 7 - n)  # Enviar datos
                time.sleep_us(80)      # Esperar 80 microsegundos
                apagar_led()
    reiniciar_juego()
def p1_win():
    """Refresca la matriz de LEDs."""
    for y in range(msgp1 + 8):           # Recorrido de tabla
        for p in range(timpoMsgWin):        # Refresco de matriz
            for n in range(8):
                H595(~mensajeP1[n + y], 1 << 7 - n)  # Enviar datos
                time.sleep_us(80)      # Esperar 80 microsegundos
                apagar_led()
    reiniciar_juego()
def refrescar_matriz():
    """Refresca la matriz de LEDs."""
    for y in range(msg + 8):           # Recorrido de tabla
        for p in range(tiempo):        # Refresco de matriz
            for n in range(8):
                if(isPlaying):
                    break
                H595(~mensaje[n + y], 1 << 7 - n)  # Enviar datos
                time.sleep_us(80)      # Esperar 80 microsegundos
                apagar_led()           # Limpiar
def H595(cat, an):
    """Envía datos al registro de desplazamiento."""
    for i in range(8):
        pinData.value((an >> i) & 1)  # Enviar 'an' bit a bit
        pinClock.value(1)               # Pulso de reloj
        pinClock.value(0)
    
    for i in range(8):
        pinData.value((cat >> i) & 1)  # Enviar 'cat' bit a bit
        pinClock.value(1)               # Pulso de reloj
        pinClock.value(0)
    
    pinLatch.value(1)                  # Latch
    pinLatch.value(0)

def apagar_led():
    """Apaga todos los LEDs."""
    H595(0, 0)              # Envía un byte con todos los bits en 0

def encenderMatriz(b1, b2, b3, b4, b5, b6, b7, b8):
    for n in range(tiempo):
        H595(~b1, 1 << 0)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b2, 1 << 1)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b3, 1 << 2)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b4, 1 << 3)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b5, 1 << 4)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b6, 1 << 5)
        time.sleep_us(80)      # Esper ar 80 microsegundos
        H595(~b7, 1 << 6)
        time.sleep_us(80)      # Esperar 80 microsegundos
        H595(~b8, 1 << 7)
        time.sleep_us(80)      # Esperar 80 microsegundos
        apagar_led()
# Coision de la bola
def rellenar_ceros(binario, longitud):
    # Rellenar con ceros a la izquierda hasta alcanzar la longitud deseada
    while len(binario) < longitud:
        binario = '0' + binario
    return binario

def colisionP1(ant):                                                                       
    # Número decimal
    decimal_value = game[0]  # Ejemplo de valor decimal
    decimal_value_2 = ant
    
    # Verificar que los valores son enteros
    if not isinstance(decimal_value, int) or not isinstance(decimal_value_2, int):
        print("Error: Los valores no son enteros.")
        return False
    
    # Convertir a string binario de 8 bits usando bin()
    binary_string = bin(decimal_value)[2:]  # [2:] para quitar '0b'
    binary_string_2 = bin(decimal_value_2)[2:]  # [2:] para quitar '0b'
    
    # Rellenar con ceros a la izquierda
    binary_string = rellenar_ceros(binary_string, 8)
    binary_string_2 = rellenar_ceros(binary_string_2, 8)
    
    print("String binario 1:", binary_string)
    print("String binario 2:", binary_string_2)
    
    # Comparar casilla por casilla
    for i in range(len(binary_string)):
        if binary_string[i] == binary_string_2[i] and binary_string_2[i] != '0':
            return True
    return False

def colisionP2(ant):                                                                       
    # Número decimal
    decimal_value = game[7]  # Ejemplo de valor decimal
    decimal_value_2 = ant
    
    # Verificar que los valores son enteros
    if not isinstance(decimal_value, int) or not isinstance(decimal_value_2, int):
        print("Error: Los valores no son enteros.")
        return False
    
    # Convertir a string binario de 8 bits usando bin()
    binary_string = bin(decimal_value)[2:]  # [2:] para quitar '0b'
    binary_string_2 = bin(decimal_value_2)[2:]  # [2:] para quitar '0b'
    
    # Rellenar con ceros a la izquierda
    binary_string = rellenar_ceros(binary_string, 8)
    binary_string_2 = rellenar_ceros(binary_string_2, 8)
    
    print("String binario 1:", binary_string)
    print("String binario 2:", binary_string_2)
    
    # Comparar casilla por casilla
    for i in range(len(binary_string)):
        if binary_string[i] == binary_string_2[i] and binary_string_2[i] != '0':
            return True
    return False
# Movimiento de la bola
def ballMovementRight(ballX, ballY):
    game[ballX] = 0
    ballX += 1
    game[ballX] = ballY
    return ballX

def ballMovementLeft(ballX, ballY):
    game[ballX] = 0
    ballX -= 1
    game[ballX] = ballY
    return ballX

def ballMovementDown(ballY):
    return ballY * 2

def ballMovementUp(ballY):
    return ballY // 2

# Variables de juego
x = 3
y = 1
der = True
up = False

# Variables de los jugadores
btnP2Down = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
btnP2Up = Pin("GP20", Pin.IN, Pin.PULL_DOWN)
btnP1Down = Pin("GP19", Pin.IN, Pin.PULL_DOWN)
btnP1Up = Pin("GP18", Pin.IN, Pin.PULL_DOWN)
btnReset = Pin("GP0", Pin.IN, Pin.PULL_DOWN)  # Nuevo botón para reiniciar
isPlaying = False
plyr1Position = 24
plyr2Position = 24

def plyr1Down(pos):
    if pos != 192:
        pos *= 2
        game[0] = pos
    return pos

def plyr1Up(pos):
    if pos != 3:
        pos = pos // 2
        game[0] = pos
    return pos

def plyr2Down (pos):
    if pos != 192:
        pos *= 2
        game[7] = pos
    return pos

def plyr2Up(pos):
    if pos != 3:
        pos = pos // 2
        game[7] = pos
    return pos

def reiniciar_juego():
    global x, y, der, up, tiempo, running, game, plyr1Position, plyr2Position
    
    # Restablecer las variables del juego
    x = 3
    y = 8
    der = True
    up = False
    tiempo = 100
    game = [24, 0, 0, 0, 0, 0, 0, 24]  # Restablecer el estado del juego
    plyr1Position = 24
    plyr2Position = 24
    running = True  # Reiniciar el estado de ejecución

def juego():
    global x, y, der, up, tiempo, running
    collide = False
    anterior = 0
    while running:
        if not isPlaying:
            refrescar_matriz()
        else:
            encenderMatriz(game[0], game[1], game[2], game[3], game[4], game[5], game[6], game[7])
            if der == True:
                x = ballMovementRight(x, y)
            elif der == False:
                x = ballMovementLeft(x, y)
            if collide:
                print(x)
                if not colisionP2(anterior) and x == 5:
                    p2_win()
                elif not colisionP1(anterior) and x == 2:
                    p1_win()
                collide = False
            if x >= 6:
                collide = True
                anterior = game[6]
                randNum = random.randint(1, 2)
                der = False
                if randNum == 1 and y != 1 and y != 128:
                    up = True
                else:
                    up = False
            if x <= 1:
                collide = True
                anterior = game[1]
                randNum = random.randint(1, 2)
                der = True
                if randNum == 1 and y != 1 and y != 128:
                    up = True
                else:
                    up = False
            if up == False:
                y = ballMovementDown(y)
            if up == True:
                y = ballMovementUp(y)
            if y >= 128:
                up = True
            if y <= 1:
                up = False
            # Manejo de dificultad
            tiempo -= 1
            if tiempo == 74:
                tiempo = 75
_thread.start_new_thread(juego,())

while True:
    if btnReset.value():  # Verifica si se presiona el botón de reinicio
        print('Reset')
        isPlaying = not isPlaying
        time.sleep_ms(500)
        reiniciar_juego()  # Llama a la función de reinicio
    if isPlaying:
        if btnP2Up.value():
            print('presseed 1 UP')
            plyr1Position = plyr1Up(plyr1Position)
        if btnP2Down.value():
            plyr1Position = plyr1Down(plyr1Position)
            print('pressed 1 Down')
        if btnP1Up.value():
            plyr2Position = plyr2Up(plyr2Position)
            print('pressed 2 UP')
        if btnP1Down.value():
            plyr2Position = plyr2Down(plyr2Position)
            print('pressed 2 Down')
    time.sleep_ms(200)
