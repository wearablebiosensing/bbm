

class BodySensor:

    def __init__(self, location, state):
        self.locate = location #where on the body the sensor is placed
        self.status = state #state of sensor
        self.name = "unnamed"

    def getLocation(self):
        return self.locate

    def setLocation(self, location):
        self.locate = location

    def getState(self):
        return self.status

    def setState(self, state):
        self.status = state

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def drawSensor(self,canvas,xb,yb,xe,ye):
        if self.status:
            fill = "green"
        else:
            fill = "grey"
        icon = canvas.create_oval(xb,yb,xe,ye,fill=fill)
