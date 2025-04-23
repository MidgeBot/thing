import tkinter as tk
import random

root = tk.Tk()
root.title("VariVirus")
root.geometry("1200x800")

ticker = 0
gridlinePositions = []

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

displayNum = tk.Text(leftPanel, height = 20, width = 20, font = ("Ariel", 12))
displayNum.pack(pady = 10, padx = 10, fill = "x")
displayNum.insert("end", "values ?")
displayNum.config(state = "disabled")

#right panel
rightPanel = tk.Frame(mainFrame, bg = "white", bd = 1, relief = "solid")
rightPanel.pack(side = "right", fill = "both", expand = True)

rightUpperBox = tk.Frame(rightPanel, bg = "white", bd = 1, relief = "solid")
rightUpperBox.pack(fill = "both", expand = True, padx = 10, pady = (10, 5))

rightUpperLeftCanvas = tk.Canvas(rightUpperBox, bg = "white", height = 100)
rightUpperLeftCanvas.pack(side = "left", fill = "both", expand = True)

rightUpperRightCanvas = tk.Canvas(rightUpperBox, bg = "white", height = 100)
rightUpperRightCanvas.pack(side = "left", fill = "both", expand = True)

rightLowerBox = tk.Frame(rightPanel, height = 200, bg = "lightgrey", highlightbackground = "black", highlightthickness = 1)
rightLowerBox.pack(fill = "x", padx = 10, pady = (0,10))

#timeline shenanigans
timelineCanvas = tk.Canvas(rightLowerBox, bg = "white", height = 200)
timelineCanvas.pack(fill = "both", padx = 5, pady = 5)

def timelineGrid(event = None):
    global gridlinePositions

    timelineCanvas.delete("all")
    gridCount = 17

    canvasWidth = timelineCanvas.winfo_width()
    gridSpacing = canvasWidth / (gridCount - 1)

    gridlinePositions =[]

    for i in range(gridCount):
        x = i * gridSpacing
        gridlinePositions.append(x)
        timelineCanvas.create_line(x, 0, x, 200, fill = "Lightgrey")

timelineCanvas.bind("<Configure>", timelineGrid)

timelineGrid()

timelineRunning = False
timelineCount = 0
lastPoint = None

def timelineUpdate():
    global timelineRunning, timelineCount, lastPoint, ticker

    if not timelineRunning:
        return
    if ticker >= 17:
        timelineRunning = False
        button3.config(text = "Sim done")
        return
    if ticker >= len(gridlinePositions):
        return
   
    xPos = gridlinePositions[ticker]
    yPos = random.randint(30, 170) #CHANGE THIS WHEN WE GET ACTAUL NUMBERS IDK
    rDot = 4

    timelineCanvas.create_oval(xPos - rDot, yPos - rDot, xPos + rDot, yPos + rDot, fill = "red")
    
    if lastPoint is not None:
        timelineCanvas.create_line(lastPoint[0], lastPoint[1], xPos, yPos, fill = "blue", width = 2)
   
    lastPoint = (xPos, yPos)
    displayNum.config(state = "normal")
    displayNum.insert("end", f"Day {ticker} x={int(xPos)}, y={int(yPos)}\n")
    displayNum.see("end")
    displayNum.config(state = "disabled")

    ticker += 1
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