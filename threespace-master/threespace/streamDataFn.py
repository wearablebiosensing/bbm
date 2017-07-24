# The function defined in this code will be used to stream data from a single MoCap
# sensor. The function will be called by a GUI with start stream and stop stream options
# Rassoul Diouf, Wearable Biosensing Lab, University of Rhode Island, 6/12/2017.

def streamData(streaming):
   
    # Create a string with current time, with format month-date-year_hours.minutes.
    # seconds. The following line uses the date in the name of a file created with the
    # command file=open(...). Every time the code is run, a new file will be created
    # with its name containing the exact time at which it was run

    if streaming is True:
        timestr = time.strftime('%m-%d-%Y_%H.%M.%S')
        file = open(timestr + str(fileName),"w")


    # Obtain the list of devices connected to the COM ports. Since we're only using
    # one, we chose the index 0. Then the dongle is going to correspond to that port.
        dl = ts.getComPorts()
        comPort = dl[0]
        dngDevice = ts.TSDongle(com_port=comPort)


    # Each dongle is connected to up to 15 sensors. So the following for-loop iterates
    # through all of them to see which ones are connected or not.
        for i in range(0,14):
            if dngDevice[i] is not None:
                wlDevice = dngDevice[i]


    # Now, the name of the specific sensor used is going to go on top of the file. Then
    # each slot of the stream is going to be labeled.
        file.write(str(wlDevice))
        file.write("\n\n\n")    # each "\n" skips one line


        # In the following line, R represents a real number, i, j and k representing
        # cartesian coordinates (Quarternion orientation, as seen below).
        file.write("           R,                   i,                  j,                    k,        %,  Button")
        file.write("\n\n")

        if wlDevice is not None:
            # Here, 3 slots are created
            wlDevice.setStreamingTiming(interval=0, duration=100000000, delay=0)
            wlDevice.setStreamingSlots(slot0='getTaredOrientationAsQuaternion', # 1st slot gets the orientation readings
                                       slot1='getBatteryPercentRemaining',      # 2nd gets the battery level
                                       slot2='getButtonState')                  # 3rd gets the state of the buttons

            while streaming is True:                # When start button is pressed   
                data = wlDevice.getStreamingBatch() # Stream the data as defined by the slots.
                file.write(str(data))               # Write the data in the file created
                file.write("\n")

        file.close()    # Close the file
                
        dngDevice.close()   # Close the device

