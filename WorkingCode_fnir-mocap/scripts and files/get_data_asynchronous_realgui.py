## Reading a YEI 3-Space Sensor device's orientation with streaming using
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API
from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream


#Table Chart
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,2)
        t.pack(side="top", fill="x")
        t.set(0,0,"IT WORKS")

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

if __name__ == "__main__":
    app = ExampleApp()


def connect():
    print("its just a test")
    ################################################################################
    ################# Second using a broadcaster to get streaming ##################
    ################# data for every 3-Space Sensor device known ###################
    ################################################################################
    print("=============================")
    print("Broadcaster calls")
    print("=============================")
    device_list = ts_api.getComPorts()

    all_list = []
    sensor_list = []
    chosen_sensor_list = []

    l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
    hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = True
    r_upper_leg = r_lower_leg = r_foot = True

    sensorID_string_to_sensorName = {
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
                        if sensorID_string_to_sensorName.get("'"+str(sens)+"'") is True:
                            chosen_sensor_list.append(sens)

    with open('mocapData.txt', 'w') as f:
        f.write(str(chosen_sensor_list)+'\n\n')
    f.close()


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
    print("Looking for fNIR stream...")

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
    return start2    

def fnirStart():
    global stream_inlet, fnirFlag
    print('\n fNIR streaming...')
    
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
    return (stop1, stop2)

def disconnect():
    disconnect1=ts_api.global_broadcaster.stopStreaming()
    ## Now close the ports.
    for device in all_list:
        device.close()
    print("======left all devices=========")
    return (disconnect1)

def nothing():
    print('not')

def reset():
    for wlDevice in sensor_list:
        wlDevice.clearRecordingData()
    print("=====Reset completed=====")
    return reset

#Window
root=Tk()

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
insertButton = Button(toolbar, text="Start", command=start)#while is true, stream
insertButton.pack(side=LEFT, padx=5, pady=50)
#insertButton.config( height = 10, width = 10 )
printButton= Button(toolbar, text="Stop", command=stop)#pause, then wait fot start
printButton.pack(side=LEFT, padx=5, pady=50)
#printButton.config( height = 50, width = 10 )
resetButton=Button(toolbar,text="Reset", command=reset)
resetButton.pack(side=LEFT, padx=5, pady=50)
#resetButton.config( height = 50, width = 10 )
connectButton=Button(toolbar,text="Connect", command=connect)
connectButton.pack(side=LEFT, padx=5, pady=50)
#connectButton.config( height = 50, width = 10 )
disconnectButton=Button(toolbar,text="Disconnect", command=disconnect)
disconnectButton.pack(side=LEFT, padx=5, pady=50)
#disconnectButton.config( height = 50, width = 10 )
toolbar.pack(side=BOTTOM, fill=X)

device_list = []

all_list = []
sensor_list = []

#root window
root.title("Graphical User Interface")
root.geometry("700x600")

        
root.mainloop()


