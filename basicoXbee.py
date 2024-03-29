from xbee.thread import XBee
import time
import serial

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

def message_received(data):
    print(data)
    #print(type(data))
    print(data['source_addr'])
    print(type('source_addr'))
# Create API object, which spawns a new thread
xbee = XBee(ser, callback=message_received)

# Do other stuff in the main thread
while True:
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        break

# halt() must be called before closing the serial
# port in order to ensure proper thread shutdown
xbee.halt()
ser.close()