# This code will allow a YEI 3-space sensor the stream data to a text file. This is a preleminary step, the goal
# being to eventually stream the sensor readings through a wireless network for IoT applications.
# Rassoul Diouf, Wearable Biosensing Lab, University of Rhode Island, 6/7/2017.

# Import libraries needed for this function
import threespace as ts         # Yei 3-space sensors library, with the alias ts
import time                     # Time library to use computer clock and other time-related functions


# Create a string with current time, with format month-date-year_hours.minutes.seconds. The following line uses
# the date in the name of a file created with the command file=open(...).
# Every time the code is run, a new file will be created with its name containing the exact time at which it was
# run
timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
file = open(timestr + '_YeiSensorData.txt',"w")


# Obtain the list of devices connected to the COM ports. Since we're only using one, we chose the index 0.
# Then the dongle is going to correspond to that port.
dl = ts.getComPorts()
comPort = dl[0]
dngDevice = ts.TSDongle(com_port=comPort)


# Each dongle is connected to up to 15 sensors. So the following for-loop iterates through all of them to see
# which ones are connected or not. Again, we're testing one sensor, so the varialble named wlDevice does not
# need to be have indices.
for i in range(0,14):
    if dngDevice[i] is not None:
        wlDevice = dngDevice[i]


# Now, the name of the specific sensor used is going to go on top of the file. Then each slot of the stream is
# going to be labeled.
file.write(str(wlDevice))
file.write("\n\n\n")    # each "\n" skips one line


# In the following line, R represents a real number, i, j and k representing cartesian coordinates (Quarternion
# orientation, as seen below).
file.write("           R,                   i,                  j,                    k,        %,  Button")
file.write("\n\n")

if wlDevice is not None:
    # Here, 3 slots are created
    wlDevice.setStreamingTiming(interval=0, duration=100000000, delay=0)
    wlDevice.setStreamingSlots(slot0='getAllRawComponentSensorData', # 1st slot gets the orientation readings
                               slot1='getBatteryPercentRemaining',      # 2nd gets the battery level
                               slot2='getButtonState')                  # 3rd gets the state of the buttons


    startTime=time.clock()      # Set a start time for the following loop. Using the real time clock
    while time.clock() - startTime < 5:     # Loop will last 5 seconds
        data = wlDevice.getStreamingBatch() # Stream the data as defined by the slots.
        file.write(str(data))               # Write the data in the file created
        file.write("\n")

file.close()    # Close the file
        
dngDevice.close()   # Close the device
