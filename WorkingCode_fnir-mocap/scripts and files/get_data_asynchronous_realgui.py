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
global l_shoulder, r_shoulder, l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
global r_upper_leg, r_lower_leg, r_foot



root=Tk()

# text box GUI
tex = Text(master=root)
tex.pack(side=TOP)
bop = Frame()
bop.pack(side=LEFT)


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

def PopUp():
    
    popup=Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("Sensor Quantity")
    label = Label(popup, text='Display Sensors')
    label.grid()
    
    global l_shoulder,r_shoulder,l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
    global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
    global r_upper_leg, r_lower_leg, r_foot
    
    global all_list, sensor_list, chosen_sensor_list
    l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
    hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = False
    r_upper_leg = r_lower_leg = r_foot = False
    
    var1=IntVar()
    var2=IntVar()
    var3=IntVar()
    var4=IntVar()
    var5=IntVar()
    var6=IntVar()
    var7=IntVar()
    var8=IntVar()
    var9=IntVar()
    var10=IntVar()
    var11=IntVar()
    var12=IntVar()
    var13=IntVar()
    var14=IntVar()
    var15=IntVar()
    var16=IntVar()
    var17=IntVar()
    var18=IntVar()
    
    c18=tk.Checkbutton(popup,text="All", variable=var18, \
                    onvalue=1,offvalue=0, height=5)
    if (var18.get()):
        var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17=1
    c18.grid(row=10,column=1)
    
    c1=tk.Checkbutton(popup,text="l_shoulder",variable=var1, \
                   onvalue=1,offvalue=0)


    if (var1.get()):
        l_shoulder=True
    c1.grid(row=1,column=0)

    c2=tk.Checkbutton(popup,text="r_shoulder",variable=var2, \
               onvalue=1,offvalue=0)
    if (var2.get()):
        r_shoulder=True
    c2.grid(row=1,column=1)

    c3=tk.Checkbutton(popup,text="l_upper_arm",variable=var3, \
                   onvalue=1,offvalue=0)
    if (var3.get()):
        l_upper_arm=True
    c3.grid(row=2,column=0)

    c4=tk.Checkbutton(popup,text="l_lower_arm",variable=var4, \
                   onvalue=1,offvalue=0)
    if (var4.get()):
        l_lower_arm=True
    c4.grid(row=3,column=0)

    c5=tk.Checkbutton(popup,text="l_hand",variable=var5, \
               onvalue=1,offvalue=0)
    if (var5.get()):
        l_hand=True
    c5.grid(row=4,column=0)

    c6=tk.Checkbutton(popup,text="r_upper_arm",variable=var6, \
                   onvalue=1,offvalue=0)
    if (var6.get()):
        r_upper_arm=True
    c6.grid(row=2,column=1)

    c7=tk.Checkbutton(popup,text="head",variable=var7, \
                onvalue=1,offvalue=0)
    if (var7.get()):
        head=True
    c7.grid(row=1,column=2)

    c8=tk.Checkbutton(popup,text="hips",variable=var8, \
               onvalue=1,offvalue=0)
    if (var8.get()):
        hips=True
    c8.grid(row=3,column=2)

    c9=tk.Checkbutton(popup,text="chest",variable=var9, \
                   onvalue=1,offvalue=0)
    if (var9.get()):
        chest=True
    c9.grid(row=2,column=2)

    c10=tk.Checkbutton(popup,text="r_lower_arm",variable=var10, \
                    onvalue=1,offvalue=0)
    if (var10.get()):
        r_lower_arm=True
    c10.grid(row=3,column=1)

    c11=tk.Checkbutton(popup,text="r_hand",variable=var11, \
                onvalue=1,offvalue=0)
    if (var11.get()):
        r_hand=True
    c11.grid(row=4,column=1)

    c12=tk.Checkbutton(popup,text="l_upper_leg",variable=var12, \
                    onvalue=1,offvalue=0)
    if (var12.get()):
        l_upper_leg=True
    c12.grid(row=6,column=0)

    c13=tk.Checkbutton(popup,text="l_lower_leg",variable=var13, \
                onvalue=1,offvalue=0)
    if (var13.get()):
        l_lower_leg=True
    c13.grid(row=7,column=0)

    c14=tk.Checkbutton(popup,text="l_foot",variable=var14, \
                onvalue=1,offvalue=0)
    if (var14.get()):
        l_foot=True
    c14.grid(row=8,column=0)

    c15=tk.Checkbutton(popup,text="r_upper_leg",variable=var15, \
                    onvalue=1,offvalue=0)
    if var15.get():
        r_upper_leg=True
    c15.grid(row=6,column=1)

    c16=tk.Checkbutton(popup,text="r_lower_leg",variable=var16, \
                    onvalue=1,offvalue=0)
    if var16.get():
        r_lower_leg=True
    c16.grid(row=7,column=1)

    c17=tk.Checkbutton(popup,text="r_foot",variable=var17, \
                onvalue=1,offvalue=0)
    if var17.get():
        r_foot=True
    c17.grid(row=8,column=1)
    

    btn1=Button(popup, text='Apply', command=sensorID_string_commit )
    btn1.grid(row=11,column=2)

    #btn1.destroy()
    
    popup.mainloop()

def sensorID_string_commit():
    global l_shoulder, r_shoulder, l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
    global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
    global r_upper_leg, r_lower_leg, r_foot
    global all_list, sensor_list, chosen_sensor_list
    global sensorID_string_to_sensorName

    device_list = ts_api.getComPorts()

    all_list = []
    sensor_list = []
    chosen_sensor_list = []
    chosen_sensor_list = []
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

    print(sensorID_string_to_sensorName)
    
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
##        tex.insert(tk.END, device_type)
##        tex.see(tk.END)
        
        if device is not None:
            all_list.append(device)
            if device_type != "DNG":
                sensor_list.append(device)
            else:
                for i in range(6): # Only checking the first six logical indexes
                    sens = device[i]
                    if sens is not None:
                        sensor_list.append(sens)
##                        tex.insert(tk.END, str(sens))
##                        tex.see(tk.END)
                        if sensorID_string_to_sensorName.get("'"+str(sens)+"'") is True:
                            chosen_sensor_list.append(sens)
    cmt=str(chosen_sensor_list)
    tex.insert(tk.END,cmt)
    tex.see(tk.END)


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

##    device_list = ts_api.getComPorts()

    global all_list, sensor_list, chosen_sensor_list
##    all_list = []
##    sensor_list = []
##    chosen_sensor_list = []
    
    global l_shoulder, r_shoulder, l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
    global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
    global r_upper_leg, r_lower_leg, r_foot

    ##l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
    ##hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = True
    ##r_upper_leg = r_lower_leg = r_foot = True


#    sensorID_string_to_sensorName = {
#        "'"+str("<YEI3Space WL:1200085A>")+"'": l_shoulder,
#        "'"+str("<YEI3Space WL:1200085B>")+"'": r_shoulder,
#        "'"+str("<YEI3Space WL:1200085C>")+"'": l_upper_arm,
#        "'"+str("<YEI3Space WL:1200085D>")+"'": l_lower_arm,
#        "'"+str("<YEI3Space WL:1200085E>")+"'": l_hand,
#        "'"+str("<YEI3Space WL:1200085F>")+"'": r_upper_arm,
#        "'"+str("<YEI3Space WL:12000857>")+"'": head,
#        "'"+str("<YEI3Space WL:12000858>")+"'": hips,
#        "'"+str("<YEI3Space WL:12000859>")+"'": chest,
#        "'"+str("<YEI3Space WL:12000860>")+"'": r_lower_arm,
#        "'"+str("<YEI3Space WL:12000861>")+"'": r_hand,
#        "'"+str("<YEI3Space WL:12000862>")+"'": l_upper_leg,
#        "'"+str("<YEI3Space WL:12000863>")+"'": l_lower_leg,
#        "'"+str("<YEI3Space WL:12000864>")+"'": l_foot,
#        "'"+str("<YEI3Space WL:12000865>")+"'": r_upper_leg,
#        "'"+str("<YEI3Space WL:12000866>")+"'": r_lower_leg,
#        "'"+str("<YEI3Space WL:12000867>")+"'": r_foot
#        }
#    for device_port in device_list:
#        com_port, friendly_name, device_type = device_port
#        device = None
#        if device_type == "USB":
#            device = ts_api.TSUSBSensor(com_port=com_port)
#        elif device_type == "DNG":
#            device = ts_api.TSDongle(com_port=com_port)
#        elif device_type == "WL":
#            device = ts_api.TSWLSensor(com_port=com_port)
#        elif device_type == "EM":
#            device = ts_api.TSEMSensor(com_port=com_port)
#        elif device_type == "DL":
#            device = ts_api.TSDLSensor(com_port=com_port)
#        elif device_type == "BT":
#            device = ts_api.TSBTSensor(com_port=com_port)
#        
#        if device is not None:
#            all_list.append(device)
#            if device_type != "DNG":
#                sensor_list.append(device)
#            else:
#                for i in range(6): # Only checking the first six logical indexes
#                    sens = device[i]
#                    if sens is not None:
#                        sensor_list.append(sens)
#                        if sensorID_string_to_sensorName.get("'"+str(sens)+"'") is True:
#                            chosen_sensor_list.append(sens)


    print("======MoCap connected success===============")
    connSuccess=("======MoCap connected success===============\n")
    tex.insert(tk.END,connSuccess)
    tex.see(tk.END)

    print("Looking for fNIR stream...")
    connSuccess=("Looking for fNIR stream...\n")
    tex.insert(tk.END,connSuccess)
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
    mocapstartColl=str("==========MoCap started collection========\n")
    tex.insert(tk.END,mocapstartColl)
    tex.see(tk.END)
    return start2

def fnirStart():
    global stream_inlet, fnirFlag
    print('\n fNIR streaming...')
    fnirsstartColl=str("==========fNIRs started collection========\n")
    tex.insert(tk.END,fnirsstartColl)
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
    stopColl=str("======stop collection===========\n")
    tex.insert(tk.END,stopColl)
    tex.see(tk.END)
    return (stop1, stop2)

def disconnect():
    disconnect1=ts_api.global_broadcaster.stopStreaming()
    ## Now close the ports.
    for device in all_list:
        device.close()
    print("======left all devices=========")
    disc=str("======all devices disconnected=========\n")
    tex.insert(tk.END,disc)
    tex.see(tk.END)
    return (disconnect1)

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
SensorButton=Button(toolbar,text="Sensors", command=PopUp)
SensorButton.pack(side=LEFT, padx=5, pady=50)

device_list = []

all_list = []
sensor_list = []

#root window
root.title("Graphical User Interface")
root.geometry("700x600")

        
root.mainloop()


