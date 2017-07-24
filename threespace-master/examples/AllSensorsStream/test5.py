import threespace as ts_api
import time

device_list = ts_api.getComPorts()


## Only one 3-Space Sensor Dongle device is needed so we are just going to
## take the first one from the list.
com_port = device_list[0]
dng_device = ts_api.TSDongle(com_port=com_port)

## If a connection to the COM port fails, None is returned.
if dng_device is not None:
    ## Now we need to get our Wireless device from our Dongle device.
    ## Indexing into the TSDongle instance like it was a list will return a
    ## TSWLSensor instance.
    for i in range(15):
        if dng_device[i] is not None:
            wl_device = dng_device[i]
    
    ## Set the stream slots for getting the tared orientation of the device as a
    ## quaternion, the raw component data, and the button state
    wl_device.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                slot1='getAllRawComponentSensorData',
                                slot2='getButtonState')
    
    ## Now we can start getting the streaming batch data from the device.
    print("==================================================")
    print("Getting the streaming batch data.")
    start_time = time.clock()
    while time.clock() - start_time < 1:
        print(wl_device.getStreamingBatch())
        print("=======================================\n")
    
    ## Now close the port.
    dng_device.close()
