## Reading a YEI 3-Space Sensor device's orientation with streaming using
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API
from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
#Window GUI
root=Tk()

# text box GUI
tex = Text(master=root)
tex.pack(side=TOP)
bop = Frame()
bop.pack(side=LEFT)

l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = False
r_upper_leg = r_lower_leg = r_foot = False

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


def connect():
    ################################################################################
    ################# Second using a broadcaster to get streaming ##################
    ################# data for every 3-Space Sensor device known ###################
    ################################################################################
##    print("=============================")
##    print("Broadcaster calls")
##    print("=============================")
    string=str('Calling Broadcaster..\n')
    tex.insert(tk.END,string)
    tex.see(tk.END)
    device_list = ts_api.getComPorts()
 

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
                        if sensorIDstring_to_sensorName.get(str(sens)) is True:
                            chosen_sensor_list.append(sens)
     


    ## The YEI 3-Space Python API has a global broadcaster called global_broadcaster
    ## which is an instance of Broadcaster

##
##    ts_api.global_broadcaster.setStreamingTiming(   interval=1000000,
##                                                    duration=4294967295,
##                                                    delay=200000,
##                                                    delay_offset=0,
##                                                    filter=sensor_list)
##    ts_api.global_broadcaster.setStreamingSlots(
##                                            slot0='getRawAccelerometerData',
##                                            slot1='getBatteryPercentRemaining',
##                                            filter=sensor_list)
##    ts_api.global_broadcaster.startStreaming(filter=sensor_list)

    connSuccess=("======connected success===============\n")
    tex.insert(tk.END,connSuccess)
    tex.see(tk.END)

def start():

    for sensor in sensor_list:
        if (sensor is not None) and (sensorIDstring_to_sensorName.get(str(sensor)) is True):
            chosen_sensor_list.append(sensor)
    
    ts_api.global_broadcaster.setStreamingTiming(   interval=1000000,
                                                    duration=4294967295,
                                                    delay=200000,
                                                    delay_offset=0,
                                                    filter=chosen_sensor_list)
    ts_api.global_broadcaster.setStreamingSlots(
                                                slot0='getRawAccelerometerData',
                                                slot1='getBatteryPercentRemaining',
                                                filter=chosen_sensor_list)
    ts_api.global_broadcaster.startStreaming(filter=chosen_sensor_list)


    start2=ts_api.global_broadcaster.startRecordingData(filter=chosen_sensor_list)
    clock=time.clock()
    startColl=str("==========started collection========\n")
    tex.insert(tk.END,startColl)
    tex.see(tk.END)
    return (start2, clock)
def stop():
    stop1=ts_api.global_broadcaster.stopRecordingData()
    stop2=ts_api.global_broadcaster.stopStreaming()
    stopColl=str("======stop collection===========\n")
    tex.insert(tk.END,stopColl)
    tex.see(tk.END)
    return (stop1, stop2)

def disconnect():
    disconnect1=ts_api.global_broadcaster.stopStreaming()
    ## Now close the ports.
    for device in all_list:
        device.close()
    disc=str("======all devices disconnected=========\n")
    tex.insert(tk.END,disc)
    tex.see(tk.END)
    return (disconnect1)

def nothing():
    print('not')

def reset():
    for wlDevice in sensor_list:
        wlDevice.clearRecordingData()
    reset=str("=====Reset completed=====\n")
    tex.insert(tk.END,reset)
    tex.see(tk.END)
    return reset
def PopUp():
    from Tkinter import*
    popup = Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("Sensor Quantity")
    label = Label(popup, text='Display Sensors')
    label.grid()



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


    c1=Checkbutton(popup,text="l_shoulder",variable=var1, \
                         onvalue=1,offvalue=0)
    if (var1==1):
        return l_shoulder
    c1.grid(row=1,column=0)
    c2=Checkbutton(popup,text="r_shoulder",variable=var2, \
                         onvalue=1,offvalue=0)
    if (var2==1):
        return r_shoulder
    c2.grid(row=1,column=1)
    c3=Checkbutton(popup,text="l_upper_arm",variable=var3, \
                         onvalue=1,offvalue=0)
    if (var3==1):
        return l_upper_arm
    c3.grid(row=2,column=0)
    c4=Checkbutton(popup,text="l_lower_arm",variable=var4, \
                         onvalue=1,offvalue=0)
    if (var4==1):
        return l_lower_arm
    c4.grid(row=3,column=0)
    c5=Checkbutton(popup,text="l_hand",variable=var5, \
                         onvalue=1,offvalue=0)
    if (var5==1):
        return l_hand
    c5.grid(row=4,column=0)
    c6=Checkbutton(popup,text="r_upper_arm",variable=var6, \
                         onvalue=1,offvalue=0)
    if (var6==1):
        return r_upper_arm
    c6.grid(row=2,column=1)
    c7=Checkbutton(popup,text="head",variable=var7, \
                         onvalue=1,offvalue=0)
    if (var7==1):
        return head
    c7.grid(row=1,column=2)
    c8=Checkbutton(popup,text="hips",variable=var8, \
                         onvalue=1,offvalue=0)
    if (var8==1):
        return hips
    c8.grid(row=3,column=2)
    c9=Checkbutton(popup,text="chest",variable=var9, \
                         onvalue=1,offvalue=0)
    if (var9==1):
        return chest
    c9.grid(row=2,column=2)
    c10=Checkbutton(popup,text="r_lower_arm",variable=var10, \
                         onvalue=1,offvalue=0)
    if (var10==1):
        return r_lower_arm
    c10.grid(row=3,column=1)
    c11=Checkbutton(popup,text="r_hand",variable=var11, \
                         onvalue=1,offvalue=0)
    if (var11==1):
        return r_hand
    c11.grid(row=4,column=1)
    c12=Checkbutton(popup,text="l_upper_leg",variable=var12, \
                         onvalue=1,offvalue=0)
    if (var12==1):
        return l_upper_leg
    c12.grid(row=6,column=0)
    c13=Checkbutton(popup,text="l_lower_leg",variable=var13, \
                         onvalue=1,offvalue=0)
    if (var13==1):
        return l_lower_leg
    c13.grid(row=7,column=0)
    c14=Checkbutton(popup,text="l_foot",variable=var14, \
                         onvalue=1,offvalue=0)
    if (var14==1):
        return l_foot
    c14.grid(row=8,column=0)
    c15=Checkbutton(popup,text="r_upper_leg",variable=var15, \
                         onvalue=1,offvalue=0)
    if (var15==1):
        return r_upper_leg
    c15.grid(row=6,column=1)
    c16=Checkbutton(popup,text="r_lower_leg",variable=var16, \
                         onvalue=1,offvalue=0)
    if (var16==1):
        return r_lower_leg
    c16.grid(row=7,column=1)
    c17=Checkbutton(popup,text="r_foot",variable=var17, \
                         onvalue=1,offvalue=0)
    if (var17==1):
        return r_foot
    c17.grid(row=8,column=1)
    c18=Checkbutton(popup,text="All", variable=var18, \
                    onvalue=1,offvalue=0, height=5)
    if (var18==1):
        var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17=1
    elif(var18==0):
        var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17=0
    c18.grid(row=10,column=1)
    btn1=Button(popup, text='Apply', command=sensorID_string_to_sensorName )
    btn1.grid(row=12,column=1)
    popup.destroy()
 
    popup.mainloop()
    

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
##status= Label(root,text="testing..", bd=1, relief=SUNKEN, anchor=W)
##status.pack(side=BOTTOM, fill=X)

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
SensorButton=Button(toolbar,text="Sensors", command=PopUp)
SensorButton.pack(side=LEFT, padx=5, pady=50)

toolbar.pack(side=BOTTOM, fill=X)

device_list = []

all_list = []
sensor_list = []

#root window
root.title("Graphical User Interface")
root.geometry("700x600")

        
root.mainloop()

