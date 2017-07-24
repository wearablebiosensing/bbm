import threespace as ts
import time        

timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
file = open(timestr + '_YeiSensorData.txt',"w")

filter_flag = ts.TSS_FIND_DNG
device_list = ts.getComPorts(filter = filter_flag)
dl = device_list

dongle_list = []
sensor_list = []

for dongle_port in dl:
    com_port, friendly_name, device_type =  dongle_port
    device = ts.TSDongle(com_port=com_port)
    dongle_list.append(device)
    for i in range(6):
        if device[i] is not None:
            sensor_list.append(device[i])

            



##ts.global_broadcaster.setStreamingTiming(interval=0,
##                                            duration=110000000,
##                                            delay=1000000,
##                                            delay_offset=12000,
##                                            filter=sensor_list)
##
##ts.global_broadcaster.setStreamingSlots( slot0='getRawAccelerometerData',
##                                         slot1='getBatteryPercentRemaining',
##                                         #slot2='TSS_TIMESTAMP_SENSOR'
##                                         filter=sensor_list)
##ts.global_broadcaster.startStreaming(filter=sensor_list)
##ts.global_broadcaster.startRecordingData(filter=sensor_list)
##time.sleep(5)
##ts.global_broadcaster.stopRecordingData(filter=sensor_list)
##ts.global_broadcaster.stopStreaming(filter=sensor_list)
##for sensor in sensor_list:
##    file.write('Sensor({0}) stream_data len={1}'.format( sensor.serial_number_hex,
##                                                    len(sensor.stream_data)))
##for device in all_list:
##    device.close()
##file.close()
##
