import threespace as ts
import time        

timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
file = open(timestr + '_YeiSensorData.txt',"w")

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
        file.write("Sensor|FW_version|HW_version|")
for i in range(0,14):
    if dng_device0[i] is not None:
        file.write("Sensor|FW_version|HW_version|")
for i in range(0,14):
    if dng_device0[i] is not None:
        file.write("Sensor|FW_version|HW_version|")

file.write("\n")
        

for i in range(0,14):
    if dng_device0[i] is not None:
        fw_version = str(dng_device0[i].getFirmwareVersionString())
        hw_version = str(dng_device0[i].getHardwareVersionString())
        file.write(str(dng_device0[i])+"|"+fw_version+"|"+hw_version+"|")
for i in range(0,14):
    if dng_device1[i] is not None:
        fw_version = str(dng_device1[i].getFirmwareVersionString())
        hw_version = str(dng_device1[i].getHardwareVersionString())
        file.write(str(dng_device1[i])+"|"+fw_version+"|"+hw_version+"|")
for i in range(0,14):
    if dng_device2[i] is not None:
        fw_version = str(dng_device2[i].getFirmwareVersionString())
        hw_version = str(dng_device2[i].getHardwareVersionString())
        file.write(str(dng_device2[i])+"|"+fw_version+"|"+hw_version+"|")

        
file.close()
dng_device0.close()
dng_device1.close()
dng_device2.close()
