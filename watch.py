
from datetime import datetime

now = datetime.now()

#current_time = now.strftime("%H:%M:%S")
current_hour = now.hour
current_min = now.minute

current_sec = now.second

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


print(f"Current Time = {toBinary(current_hour,8)} {toBinary(current_min,8)} {toBinary(current_sec,8)}")
