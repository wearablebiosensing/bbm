import threespace as ts
import time        

timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
file = open(timestr + '_YeiSensorData.txt',"w")

dl = ts.getComPorts()
comPort = dl[0]
dngDevice = ts.TSDongle(com_port=comPort)

for i in range(0,14):
    if dngDevice[i] is not None:
        wlDevice = dngDevice[i]

file.write("\n\n")

if wlDevice is not None:
    fw_version = str(wlDevice.getFirmwareVersionString())
    hw_version = str(wlDevice.getHardwareVersionString())
    battery = str(wlDevice.getBatteryPercentRemaining())
    file.write("Device Info|Sensor|Firmware Version|Hardware Version")
    file.write("\n|" + str(wlDevice) + ";")
    file.write(fw_version + ";")
    file.write(hw_version)
    file.write("\n\n")
    file.write("Raw Accelerometer Data (X, Y, Z)|Time|Battery"
               + "\n")
    
    startTime = time.clock()
    while time.clock() - startTime < 5:
        data = wlDevice.getRawAccelerometerData()
        file.write(str(data) + "|")
        file.write(str(time.clock()) + "|")
        file.write(battery + " % ")
        file.write("\n")

file.close()
        
dngDevice.close()

