import Tkinter

root = Tkinter.Tk()
root.title('Canvas')
canvas = Tkinter.Canvas(root, width=450, height=450)
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

canvas.pack()
root.mainloop()


##def draw_circle():
##    x = input("please enter the radius of the circle: ")
##    print "the radius is", x, type(x)
##    circle1 = Circle(Point(10,0), x)
##    circle1.draw(win)
