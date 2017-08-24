## Reading a YEI 3-Space Sensor device's orientation with streaming using
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API
from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream

global all_list, sensor_list, chosen_sensor_list
global process

process = ""

root=Tk()

# text box GUI
tex = Text(master=root)
tex.pack(side=TOP)
bop = Frame()
bop.pack(side=LEFT)


##get a list of available sensors for the user to select from
def getSensors():
    
    global all_list, sensor_list
    
    all_list = []
    sensor_list = []
    
    process = "retrieving sensors"
    
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


#create a popup checkbox list for user to select desired sensors
def PopUp():
    
    process = "selecting mocap sensors"
    
    global all_list, sensor_list, chosen_sensor_list
    
    chosen_sensor_list = []

    popup=Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("MoCap Sensor Select")
    label = Label(popup, text='Display Sensors')
    label.grid()


    for sensor in sensor_list:
        sensor_list[sensor] = Variable()
        l = Checkbutton(self.root, text=sensor, variable=sensor_list[sensor])
        l.pack()


    btn1=Button(popup, text='Apply', command=sensorID_string_commit )
    btn1.pack(row=11,column=2)
    
    popup.mainloop()



def sensorID_string_commit():
    global all_list, sensor_list, chosen_sensor_list
    global sensorID_string_to_sensorName
    
    for sensor in sensor_list:
        if sensor_list[sensor].get()
            chosen_sensor_list.append(sensor)
            cmt=str(chosen_sensor_list)
            tex.insert(tk.END,cmt)
            tex.see(tk.END)

    note=str("creating file for mocap")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    with open('mocapData.txt', 'w') as f:
        f.write(str(chosen_sensor_list)+'\n\n')
    f.close()



    

def mocapconnect():
    print("its just a test")
    ################################################################################
    ################# Second using a broadcaster to get streaming ##################
    ################# data for every 3-Space Sensor device known ###################
    ################################################################################
    print("=============================")
    print("Broadcaster calls")
    print("=============================")
    note=str('Calling Broadcaster..\n')
    tex.insert(tk.END,note)
    tex.see(tk.END)

    global chosen_sensor_list


    ## The YEI 3-Space Python API has a global broadcaster called global_broadcaster
    ## which is an instance of Broadcaster
    ts_api.global_broadcaster.setStreamingTiming(   interval=128041,
                                                    duration=4294967295,
                                                    delay=200000,
                                                    delay_offset=0,
                                                    filter=chosen_sensor_list)
    ts_api.global_broadcaster.setStreamingSlots(
                                                slot0='getRawAccelerometerData',
                                                slot1='getBatteryPercentRemaining',
                                                filter=chosen_sensor_list)
                                                ts_api.global_broadcaster.startStreaming(filter=chosen_sensor_list)

    print("======MoCap connected success===============")
    note=("======MoCap connected success===============\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)

def fnirconnect():
    print("Looking for fNIR stream...")
    note=("Looking for fNIR stream...\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)

    fNIR_streams = resolve_stream('type', 'NIRS')
    global stream_inlet, fnirFlag
    fnirFlag = True
    stream_inlet = StreamInlet(fNIR_streams[0])
    print('fNIR connected success')


def mocapStart():
    with open('mocapData.txt','a') as f:
        f.write('Start time: ' + str(time.clock())+'\n\n')
    f.close()
    
    start2=ts_api.global_broadcaster.startRecordingData()
    print("==========MoCap started collection========")
    note=str("==========MoCap started collection========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return start2

def fnirStart():
    global stream_inlet, fnirFlag
    print('\n fNIR streaming...')
    note=str("==========fNIRs started collection========\n")
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

    
def start():
    Thread(target = mocapStart).start()
    Thread(target = fnirStart).start()
    return True

def stop():
    global fnirFlag
    fnirFlag = False
    
    stop1=ts_api.global_broadcaster.stopRecordingData()
    stop2=ts_api.global_broadcaster.stopStreaming()
    print("======stop collection===========")
    note=str("======stop collection===========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return (stop1, stop2)

def mocapdisconnect():
    disconnect1=ts_api.global_broadcaster.stopStreaming()
    ## Now close the ports.
    for device in all_list:
        device.close()
    print("======left all devices=========")
    note=str("======all devices disconnected=========\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)
    return (disconnect1)

def nothing():
    print('not')

def reset():
    for wlDevice in sensor_list:
        wlDevice.clearRecordingData()
    print("=====Reset completed=====")
    note=str("=====Reset completed=====\n")
    tex.insert(tk.END,note)
    tex.see(tk.END)

    return reset


#Menu
menu=Menu(root)
root.configure(menu=menu)

subMenu= Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project", command=nothing)
subMenu.add_command(label="Extra", command=nothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=nothing)
editMenu=Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=nothing)


#Status Bar
status= Label(root,text=process, bd=1, relief=SUNKEN, anchor=W)
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
disconnectButton.pack(side=LEFT, padx=5, pady=50)
fnirconnectButton=Button(toolbar,text="fNIR Connect", command=fnirconnect)
fnirconnectButton.pack(side=LEFT, padx=5, pady=50)
insertButton = Button(toolbar, text="All Start", command=start)
insertButton.pack(side=LEFT, padx=5, pady=50)
printButton= Button(toolbar, text="All Stop", command=stop)
printButton.pack(side=LEFT, padx=5, pady=50)
resetButton=Button(toolbar,text="All Reset", command=reset)
resetButton.pack(side=LEFT, padx=5, pady=50)
toolbar.pack(side=BOTTOM, fill=X)


#root window
root.title("Graphical User Interface")
root.geometry("900x600")

        
root.mainloop()


