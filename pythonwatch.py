#! /bin/python

from time import sleep
from sense_hat import SenseHat
from datetime import datetime
import signal
import sys

#constants
COLORS = {'Red':(100,0,0),'Blue':(0,0,100),'Green':(0,100,0),'White':(255,255,255),'Black':(0,0,0)}
NO_OF_COLUMNS = 8
NO_OF_ROWS = 8
NO_OF_LIGHTS = NO_OF_COLUMNS*NO_OF_ROWS

#globals
hat = SenseHat()
pixels = [COLORS['Black'] for item in range(NO_OF_LIGHTS)]
mode_24 = True
mode_tens = False
running = True

def signal_term_handler(signal, frame):
    """handle shutdown from system or keyboard interrupt"""
    global hat
    hat.clear()
    hat.show_message("Programmet slutter")
    sys.exit(0)
 

def clear():
    """clears pixelarray 
    returns new array"""
    # could be optimized, by not making a new array
    return [COLORS['Black'] for item in range(NO_OF_LIGHTS)]

def getTime():
    """Gets current hour, minite and second from time
    returns tupple"""
    now = datetime.now()
    #print(now)
    return (now.hour,now.minute,now.second)

def toBinary(bytenumber, bitnumber):
    """converts number to bitstring of bitnumber length"""
    result = ''
    # not elagant to meets the right start and stop
    for n in range(bitnumber-1,-1,-1):
        if bytenumber >= 2**n:
            result += '1'
            bytenumber -= 2**n
        else:
            result += '0'
    return result

def setRow(ColumnNumber,binString,color):
    """puts binary string in row in specified color"""
    global pixels
    for index, char in enumerate(binString):
        if char == '1':
            pixels[index+ColumnNumber*NO_OF_ROWS] = color
            

def setColumn(rowNumber,binString,color):
    """puts binary string in column in specified color"""
    global pixels
    for index, char in enumerate(binString):
        if char == '1':
            pixels[index*NO_OF_ROWS+rowNumber] = color


def seperateTime(time):
    """seperates hours,minutes and seconds, by tens and ones"""
    return (seperateOnes(time[0]),seperateOnes(time[1]),seperateOnes(time[2]))

def seperateOnes(number):
    """Seperate tens and ones
    returns tupple"""
    # // Wholenumber division
    return (number//10,number%10)

def amFM(currentHour):
    # AM/PM
    if (currentHour < 12):
        setColumn(NO_OF_ROWS-1,'00000001',COLORS['White'])
    else: 
        setColumn(NO_OF_ROWS-1,'10000000',COLORS['White'])

def setClock():
    """Prepares pixels array to render"""
    global mode_tens,mode_24
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
            setColumn(3,toBinary(current_min[0],8),COLORS['Red'])
            setColumn(4,toBinary(current_min[1],8),COLORS['Red'])
            setColumn(5,toBinary(current_sec[0],8),COLORS['Green'])
            setColumn(6,toBinary(current_sec[1],8),COLORS['Green'])
        else:
            current_hour_int = current_hour[0]*10+current_hour[1]
            print(current_hour[0],current_hour[1])
            amFM(current_hour_int)

            current_hour = seperateOnes(current_hour_int%12)
            setColumn(1,toBinary(current_hour[0],8),COLORS['Blue'])
            setColumn(2,toBinary(current_hour[1],8),COLORS['Blue'])
            setColumn(3,toBinary(current_min[0],8),COLORS['Red'])
            setColumn(4,toBinary(current_min[1],8),COLORS['Red'])
            setColumn(5,toBinary(current_sec[0],8),COLORS['Green'])
            setColumn(6,toBinary(current_sec[1],8),COLORS['Green'])

def modeHandler(event):
    """Handle input events from sense-hat joystick"""
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
        #if (event.direction == 'middle'):
            # should turn off. doesn't work
            #running = False

def init():
    """Sets globals and handlers"""
    global hat,running,mode_24,mode_tens

    signal.signal(signal.SIGTERM, signal_term_handler)
    signal.signal(signal.SIGINT, signal_term_handler)

    hat.stick.direction_up = modeHandler
    hat.stick.direction_down = modeHandler
    hat.stick.direction_left = modeHandler
    hat.stick.direction_right = modeHandler
    hat.show_message("Programmet starter",0.01)

    # set mode based on start arguments 
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            mode_24 = True
            mode_tens = False
        elif sys.argv[1] == '2':
            mode_24 = True
            mode_tens = True
        elif sys.argv[1] == '3':
            mode_24 = False
            mode_tens = False
        elif sys.argv[1] == '4':
            mode_24 = False
            mode_tens = True
        else:
            pass

    running = True

def mainLoop():
    """main program loop"""
    global pixels,hat,running
    while running:
        pixels = clear()
        setClock()
        hat.set_pixels(pixels)


init()
mainLoop()
