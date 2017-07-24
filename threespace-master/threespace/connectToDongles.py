import threespace as ts
import time

def connect():
    device_list = ts.getComPorts()
    dl = device_list


    if dl[0] is not None:
        dng_device0 = ts.TSDongle(com_port = dl[0])
    if dl[1] is not None:
        dng_device1 = ts.TSDongle(com_port = dl[1])
    if dl[2] is not None:
        dng_device2 = ts.TSDongle(com_port = dl[2])


    for i in range(0,14):
        if dng_device0[i] is not None:
            wl_device0[i] = dng_device0[i]

    for i in range(0,14):
        if dng_device1[i] is not None:
            wl_device1[i] = dng_device1[i]

    for i in range(0,14):
        if dng_device2[i] is not None:
            wl_device2[i] = dng_device2[i]



    timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
    file = open(timestr + '_YeiSensorData.txt',"w")

