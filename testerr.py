import tkinter as tk

root = tk.Tk()
root.title("VariVirus")
root.geometry("1200x800")

#title code
titleFrame = tk.Frame(root, height = 50, bg = 'lightblue')
titleFrame.pack(fill='x')

titleLabel = tk.Label(titleFrame, text = "VariVirus", bg = 'lightblue', font = ("Arial", 16))
titleLabel.pack(pady = 10)

#main frame
mainFrame = tk.Frame(root)
mainFrame.pack(fill = "both", expand = True)

#left panel + button
leftPanel = tk.Frame(mainFrame, width = 150, bg = "lightgrey")
leftPanel.pack(side = "left", fill = "y")

button1Var = tk.StringVar(value = "Age group")
button1Opt = ["young", "old"]
button1 = tk.OptionMenu(leftPanel, button1Var, *button1Opt)
button1.pack(pady = 10, padx = 10, fill = "x")

button2Var = tk.StringVar(value = "Vaccinated")
button2Opt = ["yes", "No"]
button2 = tk.OptionMenu(leftPanel, button2Var, *button2Opt)
button2.pack(pady = 10, padx = 10, fill = "x")

button3 = tk.Button(leftPanel, text = "Start Sim", command = lambda: timelineStart())
button3.pack(pady = 10, padx = 10, fill = "x")

#right panel
rightPanel = tk.Frame(mainFrame, bg = "white", bd = 1, relief = "solid")
rightPanel.pack(side = "right", fill = "both", expand = True)

rightUpperBox = tk.Frame(rightPanel, bg = "white", bd = 1, relief = "solid")
rightUpperBox.pack(fill = "both", expand = True, padx = 10, pady = (10, 5))

rightLowerBox = tk.Frame(rightPanel, height = 200, bg = "lightgrey", highlightbackground = "black", highlightthickness = 1)
rightLowerBox.pack(fill = "x", padx = 10, pady = (0,10))

#timeline shenanigans
timelineCanvas = tk.Canvas(rightLowerBox, bg = "white", height = 200)
timelineCanvas.pack(fill = "both", padx = 5, pady = 5)

def timelineGrid():
    gridSize = 50
    for i in range(0, 1200, gridSize):
        timelineCanvas.create_line(i, 0, i, 200, fill = "Lightgrey")

timelineGrid()

timelineRunning = False
timelineCount = 0

def timelineUpdate():
    global timelineCount
    if not timelineRunning:
        return
    xPos = timelineCount * 50
    if xPos < 1200:
        timelineCanvas.create_rectangle(xPos, 0, xPos + 10, 200, fill = "blue")
    timelineCount += 1
    rightLowerBox.after(1000, timelineUpdate)

def timelineStart():
    global timelineRunning, timelineCount
    if not timelineRunning:
        timelineRunning = True
        timelineCount = 0 
        timelineUpdate()

#go
root.mainloop()