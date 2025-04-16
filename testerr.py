import tkinter as tk
import random

root = tk.Tk()
root.title("VariVirus")
root.geometry("1200x800")

ticker = 0

#title code
titleFrame = tk.Frame(root, height = 50, bg = 'lightblue')
titleFrame.pack(fill='x')

titleLabel = tk.Label(titleFrame, text = "VariVirus", bg = 'lightblue', font = ("Arial", 16))
titleLabel.pack(pady = 10)

#main frame
mainFrame = tk.Frame(root)
mainFrame.pack(fill = "both", expand = True)

#left panel + buttons + clock
leftPanel = tk.Frame(mainFrame, width = 150, bg = "lightgrey")
leftPanel.pack(side = "left", fill = "y")

button1Var = tk.StringVar(value = "Age group")
button1Opt = ["young", "old"]
button1 = tk.OptionMenu(leftPanel, button1Var, * button1Opt)
button1.pack(pady = 10, padx = 10, fill = "x")

button2Var = tk.StringVar(value = "Vaccinated")
button2Opt = ["yes", "No"]
button2 = tk.OptionMenu(leftPanel, button2Var, * button2Opt)
button2.pack(pady = 10, padx = 10, fill = "x")

button3 = tk.Button(leftPanel, text = "Start Sim", command = lambda: toggleSimulation())
button3.pack(pady = 10, padx = 10, fill = "x")

button4 = tk.Button(leftPanel, text = "Reset Sim", command = lambda: resetSimulation())
button4.pack(pady = 10, padx = 10, fill = "x")

clockLabel = tk.Label(leftPanel, text = f"Day: {ticker}", bg = "black", font = ("Ariel", 12))
clockLabel.pack(anchor = "center", padx = 10)

#right panel
rightPanel = tk.Frame(mainFrame, bg = "white", bd = 1, relief = "solid")
rightPanel.pack(side = "right", fill = "both", expand = True)

rightUpperBox = tk.Frame(rightPanel, bg = "white", bd = 1, relief = "solid")
rightUpperBox.pack(fill = "both", expand = True, padx = 10, pady = (10, 5))

rightUpperCanvas = tk.Canvas(rightUpperBox, bg = "white", height = 100)
rightUpperCanvas.pack(fill = "both", expand = True)

rightLowerBox = tk.Frame(rightPanel, height = 200, bg = "lightgrey", highlightbackground = "black", highlightthickness = 1)
rightLowerBox.pack(fill = "x", padx = 10, pady = (0,10))

'''
#circle, just a test to see if i can even make this work :/ old and outdated, just here for the vibes
circleRadius = 20
circleY = 50
circleLeftX = 20
circle = rightUpperCanvas.create_oval(0, 0, 0, 0, fill = "green")

circle = rightUpperCanvas.create_oval(circleLeftX - circleRadius, circleY - circleRadius, circleLeftX + circleRadius, circleY + circleRadius, fill = "green") #this is so awful i hate this

def moveCircle():
    global ticker
    canvasWidth = rightUpperCanvas.winfo_width()
    padding = 20
    
    if canvasWidth < 100:
        canvasWidth = 1200
    
    if ticker % 2 == 0:
        newX = padding #right?
    else:
        newX = canvasWidth - padding #left?
    
    rightUpperCanvas.coords(circle, newX - circleRadius, circleY - circleRadius, newX + circleRadius, circleY + circleRadius)
'''

#timeline shenanigans
timelineCanvas = tk.Canvas(rightLowerBox, bg = "white", height = 200)
timelineCanvas.pack(fill = "both", padx = 5, pady = 5)

def timelineGrid(event = None):
    timelineCanvas.delete("all")
    gridCount = 16

    canvasWidth = timelineCanvas.winfo_width()
    gridSpacing = canvasWidth / (gridCount - 1)

    for i in range(gridCount):
        x = i * gridSpacing
        timelineCanvas.create_line(x, 0, x, 200, fill = "Lightgrey")

timelineCanvas.bind("<Configure>", timelineGrid)

timelineGrid()

timelineRunning = False
timelineCount = 0
lastPoint = None

def timelineUpdate():
    global timelineCount, lastPoint, ticker
    if not timelineRunning:
        return
    xPos = ticker * 50
    if xPos >= 1200:
        return
    yPos = random.randint(30, 170) #CHANGE THIS WHEN WE GET ACTAUL NUMBERS IDK
    rDot = 4
    timelineCanvas.create_oval(xPos - rDot, yPos - rDot, xPos + rDot, yPos + rDot, fill = "red")
    if lastPoint is not None:
        timelineCanvas.create_line(lastPoint[0], lastPoint[1], xPos, yPos, fill = "blue", width = 2)
    lastPoint = (xPos, yPos)
    ticker += 1
    
    #moveCircle()

    clockLabel.config(text = f"Day: {ticker}")

    rightLowerBox.after(500, timelineUpdate)

def toggleSimulation():
    global timelineRunning, timelineCount, lastPoint
    if timelineRunning:
        timelineRunning = False
        button3.config(text = "Resume Sim")
    else:
        timelineRunning = True
        button3.config(text = "Pause Sim") 
        timelineUpdate()

def resetSimulation():
    global timelineRunning, timelineCount, lastPoint, ticker
    timelineRunning = False
    timelineCount = 0
    lastPoint = None
    ticker = 0
    clockLabel.config(text = f"Day: {ticker}")
    timelineCanvas.delete("all")
    timelineGrid()
    button3.config(text = "Start Sim")

#go
root.mainloop()