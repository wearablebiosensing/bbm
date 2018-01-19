## Reading a YEI 3-Space Sensor device's orientation with streaming using
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API
from Tkinter import*
import Tkinter as tk
import threespace_mine as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream


global all_list, sensor_list, chosen_sensor_list

root=Tk()

# text box GUI
tex = Text(master=root)
tex.pack(side=TOP)
bop = Frame()
bop.pack(side=LEFT)

sensorID_to_sensorName = {
    "<YEI3Space WL:1200085A>": "l_shoulder",
    "<YEI3Space WL:1200085B>": "r_shoulder",
    "<YEI3Space WL:1200085C>": "l_upper_arm",
    "<YEI3Space WL:1200085D>": "l_lower_arm",
    "<YEI3Space WL:1200085E>": "l_hand",
    "<YEI3Space WL:1200085F>": "r_upper_arm",
    "<YEI3Space WL:12000857>": "head",
    "<YEI3Space WL:12000858>": "hips",
    "<YEI3Space WL:12000859>": "chest",
    "<YEI3Space WL:12000860>": "r_lower_arm",
    "<YEI3Space WL:12000861>": "r_hand",
    "<YEI3Space WL:12000862>": "l_upper_leg",
    "<YEI3Space WL:12000863>": "l_lower_leg",
    "<YEI3Space WL:12000864>": "l_foot",
    "<YEI3Space WL:12000865>": "r_upper_leg",
    "<YEI3Space WL:12000866>": "r_lower_leg",
    "<YEI3Space WL:12000867>": "r_foot"
    }

#Table Chart
##class ExampleApp(tk.Tk):
    ##def __init__(self):
        ##tk.Tk.__init__(self)
        ##t = SimpleTable(self, 10,2)
        ##t.pack(side="top", fill="x")
        ##t.set(0,0,"IT WORKS")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=30)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

##if __name__ == "__main__":
##    app = ExampleApp()


def connect():
    print("its just a test")
    ################################################################################
    ################# Second using a broadcaster to get streaming ##################
    ################# data for every 3-Space Sensor device known ###################
    ################################################################################
    print("=============================")
    print("Broadcaster calls")
    print("=============================")
    string=str('Calling Broadcaster..\n')
    tex.insert(tk.END,string)
    tex.see(tk.END)

    global all_list, sensor_list, chosen_sensor_list

    device_list = ts_api.getComPorts()
    all_list = []
    sensor_list = []

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

    ## The YEI 3-Space Python API has a global broadcaster called global_broadcaster
    ## which is an instance of Broadcaster
    ts_api.global_broadcaster.setStreamingTiming(   interval=0,
                                                duration=20000000,
                                                delay=0,
                                                delay_offset=0,
                                                filter=sensor_list)
    ts_api.global_broadcaster.setStreamingSlots(
                                        slot0='getAllRawComponentSensorData',
                                        slot1='getButtonState',
                                        filter=sensor_list)

##    with open('mocapData.txt', 'w') as f:
##        f.write(str(sensor_list)+'\n\n')
##    f.close()
    
    print("======MoCap connection successful===============")
    connSuccess=("======MoCap connection successful===============\n")
    tex.insert(tk.END,connSuccess)
    tex.see(tk.END)

##    print("Looking for fNIR stream...")
##    connSuccess=("Looking for fNIR stream...\n")
##    tex.insert(tk.END,connSuccess)
##    tex.see(tk.END)
##
##    fNIR_streams = resolve_stream('type', 'NIRS')
##    global stream_inlet, fnirFlag
##    fnirFlag = True
##    stream_inlet = StreamInlet(fNIR_streams[0])
##    print('fNIR connected success')

def mocapStart():

    #start2=ts_api.global_broadcaster.startRecordingData()
    ts_api.global_broadcaster.startStreaming(filter=sensor_list)
    ts_api.global_broadcaster.startRecordingData(filter=sensor_list)

    print("==========MoCap started collection========")
    
    mocapstartColl=str("==========MoCap started collection========\n")
    tex.insert(tk.END,mocapstartColl)
    tex.see(tk.END)
    start2 =0
    return start2

def fnirStart():
    global stream_inlet, fnirFlag
    print('\n fNIR streaming...')
    fnirsstartColl=str("==========fNIRs started collection========\n")
    tex.insert(tk.END,fnirsstartColl)
    tex.see(tk.END)
    with open('fNIR_data.txt','w') as f:
        f.write('Start time: ' + str(time.clock())+'\n\n')
 
    while fnirFlag:
        sample, timestamp = stream_inlet.pull_sample()
    
def start():
    Thread(target = mocapStart).start()
    #Thread(target = fnirStart).start()
    return True

def stop():
    global fnirFlag
    fnirFlag = False
    
    stop1=ts_api.global_broadcaster.stopRecordingData(filter=sensor_list)
    stop2=ts_api.global_broadcaster.stopStreaming(filter=sensor_list)

    print("====== Stopped collection==========")

    for sens in sensor_list:
        open(sensorID_to_sensorName.get(str(sens)) + time.strftime("%Y%m%d-%H%M%S") + '.txt','w+').close()
        with open(sensorID_to_sensorName.get(str(sens)) + time.strftime("%Y%m%d-%H%M%S") + '.txt','a') as f:
            for data in sens.stream_data:
                f.write(str(data)+'\n')
    
    stopColl=str("======stop collection===========\n")
    tex.insert(tk.END,stopColl)
    tex.see(tk.END)
    return (stop1, stop2)

def disconnect():
    ## Now close the ports.
    for device in all_list:
        device.close()
    print("======all devices disconnected=========")
    disc=str("======all devices disconnected=========\n")
    tex.insert(tk.END,disc)
    tex.see(tk.END)
    return (disconnect)

def nothing():
    print('not')

def reset():
    for wlDevice in sensor_list:
        wlDevice.clearRecordingData()
    print("=====Reset completed=====")
    rst=str("=====Reset completed=====\n")
    tex.insert(tk.END,rst)
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
status= Label(root,text="testing..", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

#Tool Bar
toolbar= Frame(root)
connectButton=Button(toolbar,text="Connect", command=connect)
connectButton.pack(side=LEFT, padx=5, pady=50)
insertButton = Button(toolbar, text="Start", command=start)#while is true, stream
insertButton.pack(side=LEFT, padx=5, pady=50)
printButton= Button(toolbar, text="Stop", command=stop)#pause, then wait fot start
printButton.pack(side=LEFT, padx=5, pady=50)
disconnectButton=Button(toolbar,text="Disconnect", command=disconnect)
disconnectButton.pack(side=LEFT, padx=5, pady=50)
resetButton=Button(toolbar,text="Reset", command=reset)
resetButton.pack(side=LEFT, padx=5, pady=50)
toolbar.pack(side=BOTTOM, fill=X)

device_list = []

all_list = []
sensor_list = []

#root window
root.title("Graphical User Interface")
root.geometry("700x600")

        
root.mainloop()


