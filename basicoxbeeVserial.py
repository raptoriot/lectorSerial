import serial
import os

xbee_cache_list_api_0x83 = []
xbee_cache_list_api_0x81 = []
ser = serial.Serial()


def openSerial(port, baudrate):
    ser.port = port
    ser.baudrate = baudrate
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1  # non-block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control

    try:
        print("abriendo")
        ser.open()
        print("abriendo 2")
    except Exception as e:

        print("error open serial port: "+ str(e) )
        exit()


def getBit(int_type, offset):
    mask = 1 << offset
    if (int_type & mask):
        return True
    else:
        return False

def get_data_type(int_arr):
    return int_arr[3]


def get_xbee16(int_arr):
    return int_arr[4] * 256 + int_arr[5]


def get_rssi(int_arr):
    return int_arr[6]


def get_values_api_0x83(int_arr):
    datalist = [0, 0, 0, 0, 0, 0, 0, 0]  # a[0-6], digital
    data1 = int_arr[9]
    data2 = int_arr[10]
    ddigital = (getBit(data1, 0) or data2 > 0)
    da0 = getBit(data1, 1)
    da1 = getBit(data1, 2)
    da2 = getBit(data1, 3)
    da3 = getBit(data1, 4)
    da4 = getBit(data1, 5)
    da5 = getBit(data1, 6)
    da6 = getBit(data1, 7)
    pos = 11
    keep = True
    while pos + 1 < len(int_arr) and keep:
        keep = False
        if ddigital:
            datalist[7] = 256 * int_arr[pos] + int_arr[pos + 1]  # Digital
            pos += 2
            ddigital = False
            keep = True
        elif da0:
            datalist[0] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da0 = False
            keep = True
        elif da1:
            datalist[1] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da1 = False
            keep = True
        elif da2:
            datalist[2] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da2 = False
            keep = True
        elif da3:
            datalist[3] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da3 = False
            keep = True
        elif da4:
            datalist[4] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da4 = False
            keep = True
        elif da5:
            datalist[5] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da5 = False
            keep = True
        elif da6:
            datalist[6] = 256 * int_arr[pos] + int_arr[pos + 1]
            pos += 2
            da6 = False
            keep = True
    return datalist


def get_values_api_0x81(int_arr):
    datalist = ""
    for x in range(8, len(int_arr) - 2):
        chara = "" + str(chr(int_arr[x]))
        datalist += chara
    return datalist


###################################################################################

openSerial(os.path.realpath("/dev/ttyUSB0"), 9600)
if ser.isOpen():
    print("Opened")
    buf = []
    while (True):
        rawdata_s = ser.read(1)
        if len(rawdata_s) > 0:
            rawdata = ord(rawdata_s)
            if rawdata == 126:
                if len(buf) >= 10:
                    data_type = get_data_type(buf)
                    if data_type == 129:
                        values = get_values_api_0x81(buf)
                        xbee16 = get_xbee16(buf)
                        rssi = get_rssi(buf)
                        print("API2: " + str(buf) + " -> " + str(values))
                    # save_data_api_0x81(values,xbee16,rssi)
                    elif data_type == 131 and len(buf) >= 12:
                        values = get_values_api_0x83(buf)
                        xbee16 = get_xbee16(buf)
                        rssi = get_rssi(buf)
                        print("API0: " + str(buf) + " -> " + str(values))
                        # save_data_api_0x83(values,xbee16,rssi)
                    else:
                        print("INVALID: " + str(buf))
                buf = []
                buf.append(rawdata)
            else:
                buf.append(rawdata)

