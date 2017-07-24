import threespace as ts
import time
timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
file = open(timestr + '_YeiSensorsData.txt',"w")


dl = ts.getComPorts()
comPort = dl[0]
dngDevice = ts.TSDongle(com_port=comPort)

for i in range(0,14):
    if dngDevice[i] is not None:
        wlDevice = dngDevice[i]
file.write(str(wlDevice))
file.write("\n\n\n")
file.write("           R,                   i,                  j,                    k,        %,  Button")
file.write("\n\n")

if wlDevice is not None:
    wlDevice.setStreamingTiming(interval=0, duration=100000000, delay=0)
    wlDevice.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                               slot1='getBatteryPercentRemaining',
                               slot2='getButtonState')


    startTime=time.clock()
    while time.clock() - startTime < 5:
        data = wlDevice.getStreamingBatch()
        file.write(str(data))
        file.write("\n")
file.close()

dngDevice.close()
