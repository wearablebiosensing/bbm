## Reading a YEI 3-Space Sensor device's orientation with streaming using
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API
from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream
from PIL import ImageTk, Image



##device selection functions

##
##
##
##get a list of available sensors for the user to select from
def getSensors():
    
    all_list = []
    sensor_list = []
    
    status["text"] = "finding sensors"
    
    #find sensors available
    #put available com ports into list
    device_list = ts_api.getComPorts()
    #for each com port assign a device
    for device_port in device_list:
        com_port, friendly_name, device_type = device_port
        device = None
        if device_type == "USB":
            device = ts_api.TSUSBSensor(com_port=com_port)
        elif device_type == "DNG":
            device = ts_api.TSDongle(com_port=com_port)
        elif device_type == "WL":
            device = ts_api.TSWLSensor(com_port=com_port)
        elif device_type == "EM":
            device = ts_api.TSEMSensor(com_port=com_port)
        elif device_type == "DL":
            device = ts_api.TSDLSensor(com_port=com_port)
        elif device_type == "BT":
            device = ts_api.TSBTSensor(com_port=com_port)
        
        if device is not None:
            all_list.append(device)
        if device_type != "DNG":
            sensor_list.append(device)
        else:
            for i in range(6): # Only checking the first six logical indexes
                sens = device[i]
                if sens is not None:
                    sensor_list.append(sens)
                    newsensor=str(sens)
                    tex.insert(tk.END,newsensor)
                    tex.see(tk.END)
    status["text"] = "ready"


##
##create a popup checkbox list for user to select desired sensors
##
def PopUp():
    
    status["text"] = "selecting mocap sensors"
    
    popup=Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("MoCap Sensor Select")
    label = Label(popup, text='Display Sensors')
    label.grid()
    
    col_count = 0
    row = 0
    i = 0
    for sensor in sensor_dict:
        sensor_dict[sensor] = BooleanVar()
        print sensor_dict[sensor]
        print sensor
        print("------")
        checkdata.append(sensor_dict[sensor])
        conditionID.append(i)
        l = Checkbutton(popup, text=sensor, variable=sensor_dict[sensor], command=lambda i=i : onCheck(conditionID[i], checkdata[i], i), onvalue=True, offvalue=False)
        l.grid(row=row, column=col_count, sticky=W)
        row += 1
        i += 1
    
    
    btn1=Button(popup, text='Apply', command=sensorID_string_commit )
    btn1.grid(row=1,column=1)
    
    popup.mainloop()


##
##add selection to list
##
def onCheck(conditionID,checkData, index):
    print checkData
    print conditionID
    addSelection(sensor_dict.items()[index])

def addSelection(choice):
    chosen_sensor_list.append(choice[0])
    print choice[0]
    note=str("added"+str(choice[0])+'\n')
    tex.insert(tk.END,note)
    tex.see(tk.END)


##
##set selected sensors to list for streaming
##
def sensorID_string_commit():
    note=str("creating file for mocap\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    with open('mocapData.txt', 'w') as f:
        f.write(str(chosen_sensor_list)+'\n\n')
    f.close()





##button functions


##
##mocap connect to the selected sensor list
##
def mocapconnect():
    note=str('Calling Broadcaster..\n')
    tex.insert(tk.END,note)
    tex.see(tk.END)
    
    ## The YEI 3-Space Python API has a global broadcaster called global_broadcaster
    ## which is an instance of Broadcaster
    ts_api.global_broadcaster.setStreamingTiming(   interval=128041,
                                                 duration=4294967295,
                                                 delay=200000,
                                                 delay_offset=0,
                                                 filter=chosen_sensor_list)
    ts_api.global_broadcaster.setStreamingSlots( slot0='getRawAccelerometerData',
                                                slot1='getBatteryPercentRemaining',
                                                filter=chosen_sensor_list)
    ts_api.global_broadcaster.startStreaming(filter=chosen_sensor_list)
                                                                                             
    note=("======MoCap connected success===============\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)


##
##mocap start stream
##
def mocapStart():
    with open('mocapData.txt','a') as f:
        f.write('Start time: ' + str(time.clock())+'\n\n')
    f.close()
    
    start2=ts_api.global_broadcaster.startRecordingData()
    note=str("==========MoCap started collection========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return start2


##
##mocap stop stream and disconnect
##
def mocapdisconnect():
    disconnect1=ts_api.global_broadcaster.stopStreaming()
    ## Now close the ports.
    for device in all_list:
        device.close()
    note=str("======all mocap devices disconnected=========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return (disconnect1)


##
##fnir connect
##
def fnirconnect():
    note=("Looking for fNIR stream...\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    
    fNIR_streams = resolve_stream('type', 'NIRS')
    global stream_inlet, fnirFlag
    fnirFlag = True
    stream_inlet = StreamInlet(fNIR_streams[0])
    print('fNIR connected success')


##
##start fnir stream
##
def fnirStart():
    global stream_inlet, fnirFlag
    note=str("==========fNIRs started streaming========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    with open('fNIR_data.txt','w') as f:
        f.write('Start time: ' + str(time.clock())+'\n\n')
    f.close()

    while fnirFlag:
        sample, timestamp = stream_inlet.pull_sample()
        with open('fNIR_data.txt','a') as f:
            f.write(str(timestamp)+','+ str(sample))
            f.write('\n')
        f.close()

##
##start all streams
##
def start():
    Thread(target = mocapStart).start()
    Thread(target = fnirStart).start()
    return True


##
##stop all streams
##
def stop():
    global fnirFlag
    fnirFlag = False
    
    stop1=ts_api.global_broadcaster.stopRecordingData()
    stop2=ts_api.global_broadcaster.stopStreaming()
    note=str("======stop collection on all===========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return (stop1, stop2)

##
##reset
##
def reset():
    for wlDevice in sensor_list:
        wlDevice.clearRecordingData()
    note=str("=====Reset completed=====\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    chosen_sensor_list = []
    return reset


##
##for some fun
##
def addumanmodel():
    canvas = Canvas(root, width=450, height=450)
    canvas.create_oval(199,25,249,75, fill='gray90')
    x = 125
    y = 175
    #stick = canvas.create_line(x, y-75, x, y)
    diff_x = 25
    #stick_leg1 = canvas.create_line(x, y, x-diff_x, y+50)
    #stick_leg2 = canvas.create_line(x, y, x+diff_x, y+50)
    y=145


    #stick_arm1 = canvas.create_line(x, y-15, x-30, y-15)
    stick_LeftShoulder=canvas.create_oval(x+65,y-47,x+97,y-55)
    #stick_leg2 = canvas.create_line(x, y-15, x+30, y-15)
    stick_RightShoulder=canvas.create_oval(x+103,y-47,x+135,y-55)


    stick_LeftArm=canvas.create_oval(254,95,264,160)
    stick_RightArm=canvas.create_oval(185,95,195,160)

    stick_LeftForearm=canvas.create_oval(255,150,307,160)
    stick_RightForearm=canvas.create_oval(194,150,140,160)

    stick_LeftHand=canvas.create_oval(300,145,320,165)
    stick_RightHand=canvas.create_oval(130,145,150,165)

    body= canvas.create_oval(x+95,y+80,x+105,y-70)

    hips=canvas.create_oval(x+75,y+80,x+125,y+90)

    stick_UpperRightLeg=canvas.create_oval(192,230,205,305)
    stick_UpperLeftLeg=canvas.create_oval(245,230,258,305)

    stick_RightShin=canvas.create_oval(192,275,205,350)
    stick_RightShin=canvas.create_oval(245,275,258,350)

    stick_LeftFoot=canvas.create_oval(248,340,280,355)
    stick_RightFoot=canvas.create_oval(200,340,165,355)

    canvas.pack(side=RIGHT)



##when run as main function execute this code first
if __name__ == "__main__":
    
    checkdata = []
    conditionID = []
    chosen_sensor_list = []
    
    ## define positions as booleans
    l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
    hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = False
    r_upper_leg = r_lower_leg = r_foot = False

    sensor_dict = {
        "'"+str("<YEI3Space WL:1200085A>")+"'": l_shoulder,
        "'"+str("<YEI3Space WL:1200085B>")+"'": r_shoulder,
        "'"+str("<YEI3Space WL:1200085C>")+"'": l_upper_arm,
        "'"+str("<YEI3Space WL:1200085D>")+"'": l_lower_arm,
        "'"+str("<YEI3Space WL:1200085E>")+"'": l_hand,
        "'"+str("<YEI3Space WL:1200085F>")+"'": r_upper_arm,
        "'"+str("<YEI3Space WL:12000857>")+"'": head,
        "'"+str("<YEI3Space WL:12000858>")+"'": hips,
        "'"+str("<YEI3Space WL:12000859>")+"'": chest,
        "'"+str("<YEI3Space WL:12000860>")+"'": r_lower_arm,
        "'"+str("<YEI3Space WL:12000861>")+"'": r_hand,
        "'"+str("<YEI3Space WL:12000862>")+"'": l_upper_leg,
        "'"+str("<YEI3Space WL:12000863>")+"'": l_lower_leg,
        "'"+str("<YEI3Space WL:12000864>")+"'": l_foot,
        "'"+str("<YEI3Space WL:12000865>")+"'": r_upper_leg,
        "'"+str("<YEI3Space WL:12000866>")+"'": r_lower_leg,
        "'"+str("<YEI3Space WL:12000867>")+"'": r_foot
    }

    #base for canvas
    root=Tk()

    # text box GUI
    tex = Text(master=root)
    tex.pack(side=TOP)
    
    #Status Bar
    status= Label(root,text="starting", bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)


    #Tool Bar
    toolbar= Frame(root)
    findmocapButton=Button(toolbar,text="Find Mocap Sensors", command=getSensors)
    findmocapButton.pack(side=LEFT, padx=5, pady=50)
    SensorButton=Button(toolbar,text="Choose Mocap Sensors", command=PopUp)
    SensorButton.pack(side=LEFT, padx=5, pady=50)
    mocapconnectButton=Button(toolbar,text="Mocap Connect", command=mocapconnect)
    mocapconnectButton.pack(side=LEFT, padx=5, pady=50)
    mocapdisconnectButton=Button(toolbar,text="Mocap Disconnect", command=mocapdisconnect)
    mocapdisconnectButton.pack(side=LEFT, padx=5, pady=50)
    fnirconnectButton=Button(toolbar,text="fNIR Connect", command=fnirconnect)
    fnirconnectButton.pack(side=LEFT, padx=5, pady=50)
    insertButton = Button(toolbar, text="All Start", command=start)
    insertButton.pack(side=LEFT, padx=5, pady=50)
    printButton= Button(toolbar, text="All Stop", command=stop)
    printButton.pack(side=LEFT, padx=5, pady=50)
    resetButton=Button(toolbar,text="All Reset", command=reset)
    resetButton.pack(side=LEFT, padx=5, pady=50)
    toolbar.pack(side=BOTTOM, fill=X)
    addumanmodel()

    #root window
    root.title("Graphical User Interface")


    root.mainloop()
    status["text"] = "ready"
