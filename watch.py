#! /bin/python
# change mode to executable
# copy to somewhere with PATH
# remove file-extension
# IE /usr/bin


from time import sleep
from sense_hat import SenseHat

import signal
import sys
 
COLORS = {'Red':(100,0,0),'Blue':(0,0,100),'Green':(0,100,0),'White':(255,255,255),'Black':(0,0,0)}

NO_OF_COLUMNS = 8
NO_OF_ROWS = 8
NO_OF_LIGHTS = NO_OF_COLUMNS*NO_OF_ROWS

# modes
mode_24 = True
mode_tens = False

running = True

hat = SenseHat()


# følgende virker ikke
def signal_term_handler(signal, frame):
    global hat
    hat.show_message("Programmet slutter")
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)

pixels = [COLORS['Black'] for item in range(NO_OF_LIGHTS)]

def clear():
    return [COLORS['Black'] for item in range(NO_OF_LIGHTS)]

from datetime import datetime

def getTime():
    now = datetime.now()
    #print(now)
    return (now.hour,now.minute,now.second)

def toBinary(bytenumber, bitnumber):
    result = ''
    # not elagant to meet the right start and stop
    for n in range(bitnumber-1,-1,-1):
        if bytenumber >= 2**n:
            result += '1'
            bytenumber -= 2**n
        else:
            result += '0'
    return result

def setRow(ColumnNumber,binString,color):
    # fIX
    for index, char in enumerate(binString):
        if char == '1':
            pixels[index+ColumnNumber*NO_OF_ROWS] = color
            

def setColumn(rowNumber,binString,color):
    for index, char in enumerate(binString):
        if char == '1':
            #pixels[index+rowNumber*NO_OF_ROWS] = (125,125,125)
            # turn 
            pixels[index*NO_OF_ROWS+rowNumber] = color


def seperateTime(time):
    return (seperateOnes(time[0]),seperateOnes(time[1]),seperateOnes(time[2]))

def seperateOnes(number):
    # // Wholenumber division
    return (number//10,number%10)

def amFM(currentHour):
    # AM/PM
    if (currentHour < 12):
        setColumn(NO_OF_ROWS-1,'00000001',COLORS['White'])
    else: 
        setColumn(NO_OF_ROWS-1,'10000000',COLORS['White'])

def setClock():
    if(mode_tens):
        current_hour,current_min,current_sec = getTime()
        if (mode_24):
            # Mode mode_24 = True mode_tens = True
            setRow(1,toBinary(current_hour,8),COLORS['Blue'])
            setRow(2,toBinary(current_hour,8),COLORS['Blue'])
            setRow(3,toBinary(current_min,8),COLORS['Red'])
            setRow(4,toBinary(current_min,8),COLORS['Red'])
            setRow(5,toBinary(current_sec,8),COLORS['Green'])
            setRow(6,toBinary(current_sec,8),COLORS['Green'])
        else:
            amFM(current_hour)
            setRow(1,toBinary(current_hour%12,8),COLORS['Blue'])
            setRow(2,toBinary(current_hour%12,8),COLORS['Blue'])
            setRow(3,toBinary(current_min,8),COLORS['Red'])
            setRow(4,toBinary(current_min,8),COLORS['Red'])
            setRow(5,toBinary(current_sec,8),COLORS['Green'])
            setRow(6,toBinary(current_sec,8),COLORS['Green'])
    else:
        current_hour,current_min,current_sec = seperateTime(getTime())
        if(mode_24):
            # Mode mode_24 = True mode_tens = False
            setColumn(1,toBinary(current_hour[0],8),COLORS['Blue'])
            setColumn(2,toBinary(current_hour[1],8),COLORS['Blue'])
            setColumn(3,toBinary(current_min[1],8),COLORS['Red'])
            setColumn(4,toBinary(current_min[0],8),COLORS['Red'])
            setColumn(5,toBinary(current_sec[0],8),COLORS['Green'])
            setColumn(6,toBinary(current_sec[1],8),COLORS['Green'])
        else:
            current_hour_int = current_hour[0]*10+current_hour[1]
            print(current_hour[0],current_hour[1])
            amFM(current_hour_int)

            current_hour = seperateOnes(current_hour_int%12)
            setColumn(1,toBinary(current_hour[0],8),COLORS['Blue'])
            setColumn(2,toBinary(current_hour[1],8),COLORS['Blue'])
            setColumn(3,toBinary(current_min[1],8),COLORS['Red'])
            setColumn(4,toBinary(current_min[0],8),COLORS['Red'])
            setColumn(5,toBinary(current_sec[0],8),COLORS['Green'])
            setColumn(6,toBinary(current_sec[1],8),COLORS['Green'])


def changeMode(event):
    global mode_24, mode_tens,running
    if event.action == 'released':
        if (event.direction == 'left'):
            mode_24 = True
        elif (event.direction == 'right'):
            mode_24 = False
        if (event.direction == 'up'):
            mode_tens = True
        elif (event.direction == 'down'):
            mode_tens = False
        if (event.direction == 'middle'):
            # should turn off. doesn't work
            running = False

hat.stick.direction_up = changeMode
hat.stick.direction_down = changeMode
hat.stick.direction_left = changeMode
hat.stick.direction_right = changeMode



hat.show_message("Programmet starter",0.01)



# pixels[0] = (255,255,255)
# pixels[15] = (255,255,255)

# hat.set_pixels(pixels)
# running=False



while running:
    pixels = clear()
    setClock()
    hat.set_pixels(pixels)

    #sleep(0.5)


#List of signal is available in POSIX Signals. Note that SIGKILL cannot be caught.
