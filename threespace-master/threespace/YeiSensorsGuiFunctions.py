import threespace as ts
import time

def connectDongles():
    filter_flag = ts.TSS_FIND_DNG
    device_list = ts.getComPorts(filter = filter_flag)
    dl = device_list


    if dl[0] is not None:
        dng_device0 = ts.TSDongle(com_port = dl[0])
    if dl[1] is not None:
        dng_device1 = ts.TSDongle(com_port = dl[1])
    if dl[2] is not None:
        dng_device2 = ts.TSDongle(com_port = dl[2])

def disconnectDongles():
    dng_device0.close()
    dng_device1.close()
    dng_device2.close()

def startStream(dng_device0, dng_device1, dng_device2, boolean):
    boolean = True
    timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
    file = open(timestr + '_YeiSensorsData.txt',"w")

    for i in range(0,14):
        if dng_device0[i] is not None:
            file.write("Sensor|FW_version|HW_version||")
    for i in range(0,14):
        if dng_device1[i] is not None:
            file.write("Sensor|FW_version|HW_version||")
    for i in range(0,14):
        if dng_device2[i] is not None:
            file.write("Sensor|FW_version|HW_version||")

    file.write("\n")
            
    for i in range(0,14):
        if dng_device0[i] is not None:
            fw_version = str(dng_device0[i].getFirmwareVersionString())
            hw_version = str(dng_device0[i].getHardwareVersionString())
            file.write(str(dng_device0[i])+"|"+fw_version+"|"+hw_version+"||")
    for i in range(0,14):
        if dng_device1[i] is not None:
            fw_version = str(dng_device1[i].getFirmwareVersionString())
            hw_version = str(dng_device1[i].getHardwareVersionString())
            file.write(str(dng_device1[i])+"|"+fw_version+"|"+hw_version+"||")
    for i in range(0,14):
        if dng_device2[i] is not None:
            fw_version = str(dng_device2[i].getFirmwareVersionString())
            hw_version = str(dng_device2[i].getHardwareVersionString())
            file.write(str(dng_device2[i])+"|"+fw_version+"|"+hw_version+"||")

    file.write("\n\n")

    for i in range(0,14):
        if dng_device0[i] is not None:
            file.write("Data|Time|Battery||")
    for i in range(0,14):
        if dng_device1[i] is not None:
            file.write("Data|Time|Battery||")
    for i in range(0,14):
        if dng_device2[i] is not None:
            file.write("Data|Time|Battery||") 

    file.write("\n")

    while boolean is True:
        for i in range(0,14):
            if dng_device0[i] is not None:
                data = str(dng_device0[i].getRawAccelerometerData())
                battery = str(dng_device0[i].getBatteryPercentRemaining())
                Time = time.clock()
                file.write(data+"|"+str(Time)+"|"+battery+"%||")
        for i in range(0,14):
            if dng_device1[i] is not None:
                data = str(dng_device1[i].getRawAccelerometerData())
                battery = str(dng_device1[i].getBatteryPercentRemaining())
                Time = time.clock()
                file.write(data+"|"+str(Time)+"|"+battery+"%||")
        for i in range(0,14):
            if dng_device2[i] is not None:
                data = str(dng_device2[i].getRawAccelerometerData())
                battery = str(dng_device2[i].getBatteryPercentRemaining())
                Time = time.clock()
                file.write(data+"|"+str(Time)+"|"+battery+"%||")
        file.write("\n")
                    

def createFile():
    timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
    file = open(timestr + '_YeiSensorsData.txt',"w")

def stopStream(boolean):
    boolean = False

def reset(boolean):
    boolean = False
    file.close()
