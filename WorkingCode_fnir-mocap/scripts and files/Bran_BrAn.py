## Import modules needed for data collection: for GUI, YEI 3-space sensors API, NIRstar
## fNIRs API and data streaming

from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream

##global l_shoulder, r_shoulder, l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
##global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
##global r_upper_leg, r_lower_leg, r_foot
##global all_list, sensor_list, chosen_sensor_list
##global sensorID_string_to_sensorName
##global process
process = "Setting up"


# Initialize all booleans as false, meaning that the sensor is not selected for streaming
l_shoulder =0
r_shoulder =0
l_upper_arm =0
l_lower_arm =0
l_hand =0
r_upper_arm =0
head=0
hips =0
chest =0
r_lower_arm =0
r_hand =0
l_upper_leg =0
l_lower_leg =0
l_foot =0
r_upper_leg =0
r_lower_leg =0
r_foot = 0

## Dictionary corresponding every sensor's ID to its name (set as a boolen value) 
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

## Find devices from ports

def findDevices():
    global sensor_list, process
    process = "Looking for devices"
    status= Label(root, text=process, bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    all_list = []
    sensor_list = []


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

 ## Create a list of available MoCap sensors
       
        if device is not None:
            all_list.append(device)
            if device_type != "DNG":    
                sensor_list.append(device)
            else:
                for i in range(6):
                    sens = device[i]
                    if sens is not None:
                        sensor_list.append(sens)
                        note=str(sens)
                        tex.insert(tk.END,note)
                        tex.see(tk.END)
def toggle(var):
    if var.get():
        var.set(0)
    else:
        var.set(1)

## Create popup to select which sensors to stream from
def selectDevices():
    
    global all_list, sensor_list, chosen_sensor_list
    global var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12
    global var13, var14, var15, var16, var17, var18
    chosen_sensor_list = []

    popup=Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("MoCap Sensor Select")
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

    var1.set(0)
    var2.set(0)
    var3.set(0)
    var4.set(0)
    var5.set(0)
    var6.set(0)
    var7.set(0)
    var8.set(0)
    var9.set(0)
    var10.set(0)
    var11.set(0)
    var12.set(0)
    var13.set(0)
    var14.set(0)
    var15.set(0)
    var16.set(0)
    var17.set(0)
    var18.set(0)

    c1=Checkbutton(popup,text="l_shoulder",variable=var1, \
                         onvalue=1,offvalue=0,command=toggle(var1))
    c1.grid(row=1,column=0)
    c2=Checkbutton(popup,text="r_shoulder",variable=var2, \
                         onvalue=1,offvalue=0)
    c2.grid(row=1,column=1)
    c3=Checkbutton(popup,text="l_upper_arm",variable=var3, \
                         onvalue=1,offvalue=0)
    c3.grid(row=2,column=0)
    c4=Checkbutton(popup,text="l_lower_arm",variable=var4, \
                         onvalue=1,offvalue=0)
    c4.grid(row=3,column=0)
    c5=Checkbutton(popup,text="l_hand",variable=var5, \
                         onvalue=1,offvalue=0)
    c5.grid(row=4,column=0)
    c6=Checkbutton(popup,text="r_upper_arm",variable=var6, \
                         onvalue=1,offvalue=0)
    c6.grid(row=2,column=1)
    c7=Checkbutton(popup,text="head",variable=var7, \
                         onvalue=1,offvalue=0)
    c7.grid(row=1,column=2)
    c8=Checkbutton(popup,text="hips",variable=var8, \
                         onvalue=1,offvalue=0)
    c8.grid(row=3,column=2)
    c9=Checkbutton(popup,text="chest",variable=var9, \
                         onvalue=1,offvalue=0)
    c9.grid(row=2,column=2)
    c10=Checkbutton(popup,text="r_lower_arm",variable=var10, \
                         onvalue=1,offvalue=0)
    c10.grid(row=3,column=1)
    c11=Checkbutton(popup,text="r_hand",variable=var11, \
                         onvalue=1,offvalue=0)
    c11.grid(row=4,column=1)
    c12=Checkbutton(popup,text="l_upper_leg",variable=var12, \
                         onvalue=1,offvalue=0)
    c12.grid(row=6,column=0)
    c13=Checkbutton(popup,text="l_lower_leg",variable=var13, \
                         onvalue=1,offvalue=0)
    c13.grid(row=7,column=0)
    c14=Checkbutton(popup,text="l_foot",variable=var14, \
                         onvalue=1,offvalue=0)
    c14.grid(row=8,column=0)
    c15=Checkbutton(popup,text="r_upper_leg",variable=var15, \
                         onvalue=1,offvalue=0)
    c15.grid(row=6,column=1)
    c16=Checkbutton(popup,text="r_lower_leg",variable=var16, \
                         onvalue=1,offvalue=0)
    c16.grid(row=7,column=1)
    c17=Checkbutton(popup,text="r_foot",variable=var17, \
                         onvalue=1,offvalue=0)
    c17.grid(row=8,column=1)
    c18=Checkbutton(popup,text="All", variable=var18, \
                    onvalue=1,offvalue=0, height=5)
    c18.grid(row=10,column=1)
    btn1=Button(popup, text='Apply', command=applyButton )
    btn1.grid(row=12,column=1)
 
    popup.mainloop()

##def toggle(var):
##    if var.get():
##        var.set(0)
##    else:
##        var.set(1)



## Create list of selected MoCap sensors
def applyButton():
    global process
    global var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12
    global var13, var14, var15, var16, var17, var18
    
    process = "Applying"
    status= Label(root, text=process, bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    print(str(var1) + ' ' + str(var2))
    if (var18!=0):
        var1=var2=var3=var4=var5=var6=var7=var8=var9=var10=var11=var12=var13=var14=var15=var16=var17=1
    if (var1!=0):
        l_shoulder = 1

    if (var2!=0):
        r_shoulder = 1
    
    if (var3!=0):
        l_upper_arm = 1
    
    if (var4!=0):
        l_lower_arm = 1
    
    if (var5!=0):
        l_hand = 1

    if (var6!=0):
        r_upper_arm = 1

    if (var7!=0):
        head = 1
 
    if (var8!=0):
        hips = 1
    
    if (var9!=0):
        chest = 1
  
    if (var10!=0):
        r_lower_arm = 1
   
    if (var11!=0):
        r_hand = 1

    if (var12!=0):
        l_upper_leg

    if (var13!=0):
        l_lower_leg

    if (var14!=0):
        l_foot = 1

    if (var15!=0):
        r_upper_leg = 1

    if (var16!=0):
        r_lower_leg = 1
    
    if (var17!=0):
        r_foot = 1

    print(str(r_shoulder) + '\n' +  str(l_shoulder)+ '\n' +  str(chest))

    for sensor in sensor_list:
        if (sensor is not None) and (sensorID_string_to_sensorName.get("'"+str(sensor)+"'") is 1):
            print('sensor')
            


    ## Set data streaming parameters, using the desired MoCap sensors


    ## Stream MoCap data



## GUI setup
## find/connect to sensors | select MoCap sensors | connect to MoCap | prep for streaming
## stream | disconnect | reset
## Notification window
## Canvas

root=Tk()

# text box GUI
tex = Text(master=root)
tex.pack(side=TOP)
bop = Frame()
bop.pack(side=LEFT)
#Menu
menu=Menu(root)
root.configure(menu=menu)

#Status Bar
status= Label(root, text=process, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

#Tool Bar
toolbar= Frame(root)

findDevicesButton = Button(toolbar, text="Find Devices", command=findDevices)
findDevicesButton.pack(side=LEFT, padx=5, pady=50)

selectDevicesButton = Button(toolbar, text="Select Devices", command=selectDevices)#while is true, stream
selectDevicesButton.pack(side=LEFT, padx=5, pady=50)
toolbar.pack(side=BOTTOM, fill=X)


#root window
root.title("Graphical User Interface")
root.geometry("700x600")

root.mainloop()
