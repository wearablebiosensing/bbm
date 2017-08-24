## Import modules needed for data collection: for GUI, YEI 3-space sensors API, NIRstar
## fNIRs API and data streaming

from Tkinter import*
import Tkinter as tk
import threespace as ts_api
import time
import threading
from threading import Thread
from pylsl import StreamInlet, resolve_stream

global l_shoulder, r_shoulder, l_upper_arm, l_lower_arm, l_hand, r_upper_arm, head
global hips, chest, r_lower_arm, r_hand, l_upper_leg, l_lower_leg, l_foot
global r_upper_leg, r_lower_leg, r_foot
global all_list, sensor_list, chosen_sensor_list
global sensorID_string_to_sensorName


# Initialize all booleans as false, meaning that the sensor is not selected for streaming
l_shoulder = r_shoulder = l_upper_arm = l_lower_arm = l_hand = r_upper_arm = head= False
hips = chest = r_lower_arm = r_hand = l_upper_leg = l_lower_leg = l_foot = False
r_upper_leg = r_lower_leg = r_foot = False

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
    
    global sensor_list
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



## Create popup to select which sensors to stream from
def selectDevices():
    
    global all_list, sensor_list, chosen_sensor_list
    
    chosen_sensor_list = []

    popup=Tk()
    popup.geometry('250x400')
    popup.grid()
    popup.title("MoCap Sensor Select")
    label = Label(popup, text='Display Sensors')
    label.grid()


    for sensor in sensor_list:
        sensorID_string_to_sensorName.set("'"+str(sensor)+"'") = Variable()
        l = Checkbutton(popup, text=str(sensor),
                        variable=sensorID_string_to_sensorName.get("'"+str(sensor)+"'")
        label.pack()


    btn1=Button(popup, text='Apply', command=applyButton )
    btn1.pack(row=11,column=2)
    
    popup.mainloop()
    



## Create list of selected MoCap sensors
def applyButton():
    for sensor in sensor_list:
        if (sensor is not None) and (sensorID_string_to_sensorName.get("'"+str(sensor)+"'") is True):
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
status= Label(root,text="testing..", bd=1, relief=SUNKEN, anchor=W)
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
