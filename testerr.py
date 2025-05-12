import tkinter as tk
from PIL import Image, ImageTk
import random

root = tk.Tk()
root.title("VariVirus")
root.geometry("1200x800")

#variables
ticker = 0 #what day are we on
dayCount = 17 #max day count
gridlinePositions = []
dataPoints = []

#user entered variables NOT HOOKED UP TO ANYTHING YET but i think they go here. maybe.
ageGroup = None
vaccineStatus = None

frames = []
frameCount = 0
currentFrame = 0
frameDelay = 50 #ms per frame
isPlaying = False

#title 
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

button1Var = tk.StringVar(value = "Age group") #Age group
button1Opt = ["young", "old"]
button1 = tk.OptionMenu(leftPanel, button1Var, * button1Opt)
button1.pack(pady = 10, padx = 10, fill = "x")

button2Var = tk.StringVar(value = "Vaccinated") #vaccinated
button2Opt = ["yes", "No"]
button2 = tk.OptionMenu(leftPanel, button2Var, * button2Opt)
button2.pack(pady = 10, padx = 10, fill = "x")

button3 = tk.Button(leftPanel, text = "Start Sim", command = lambda: toggleSimulation()) #start sim/pause sim depending on state
button3.pack(pady = 10, padx = 10, fill = "x")

button4 = tk.Button(leftPanel, text = "Reset Sim", command = lambda: resetSimulation()) #reset sim
button4.pack(pady = 10, padx = 10, fill = "x")

clockLabel = tk.Label(leftPanel, text = f"Day: {ticker}", bg = "black", font = ("Ariel", 12)) #day counter
clockLabel.pack(anchor = "center", padx = 10)

displayNum = tk.Text(leftPanel, height = 20, width = 20, font = ("Ariel", 12)) #value outputs
displayNum.pack(pady = 10, padx = 10, fill = "x")
displayNum.insert("end", "values: \n")
displayNum.config(state = "disabled")

#right panel
rightPanel = tk.Frame(mainFrame, bg = "white", bd = 1, relief = "solid")
rightPanel.pack(side = "right", fill = "both", expand = True)

rightUpperBox = tk.Frame(rightPanel, bg = "white", bd = 1, relief = "solid")
rightUpperBox.pack(fill = "both", expand = True, padx = 10, pady = (10, 5))

leftPane = tk.Frame(rightUpperBox, bg = "white")
leftPane.pack(side = "left", fill = "both", expand = True)

rightPane = tk.Frame(rightUpperBox, bg = "white")
rightPane.pack(side = "left", fill = "both", expand = True)

rightTitle = tk.Label(rightPane, text = "rightie", bg = "lightblue", font = ("Arial", 12))
rightTitle.pack(fill = "x")

leftTitle = tk.Label(leftPane, text = "leftie", bg = "lightblue", font = ("Arial", 12))
leftTitle.pack(fill = "x")

rightUpperLeftCanvas = tk.Canvas(leftPane, bg = "white", height = 100)
rightUpperLeftCanvas.pack(side = "left", fill = "both", expand = True)

rightUpperRightCanvas = tk.Canvas(rightPane, bg = "white", height = 100)
rightUpperRightCanvas.pack(side = "left", fill = "both", expand = True)

#timeline 
rightLowerBox = tk.Frame(rightPanel, height = 200, bg = "lightgrey", highlightbackground = "black", highlightthickness = 1)
rightLowerBox.pack(fill = "x", padx = 10, pady = (0,10))

timelineCanvas = tk.Canvas(rightLowerBox, bg = "white", height = 200)
timelineCanvas.pack(fill = "both", padx = 5, pady = 5)


def timelineGrid(event = None): #draws the gridelines + adds in the actual line
    global gridlinePositions

    timelineCanvas.delete("all")
    timelineWidth = timelineCanvas.winfo_width()
    timelineSpacing = timelineWidth / dayCount
    gridlinePositions = [i * timelineSpacing for i in range (dayCount + 1)] #ew yuck

    for x in gridlinePositions:
        timelineCanvas.create_line(x, 0, x, 200, fill = "lightblue")

    last = None
    r = 4
    for day, y in dataPoints:
        x = gridlinePositions[day]
        timelineCanvas.create_oval(x - r, y - r, x + r, y + r, fill = "red")
        if last:
            timelineCanvas.create_line(last[0], last[1], x, y, fill = "blue", width = 2)
        last = (x, y)


def loadGif(path):
    global frames
    frames = []
    img = Image.open(path)

    try:
        while True:
            frame = ImageTk.PhotoImage(img.copy().convert("RGBA"))
            frames.append(frame)
            img.seek(len(frames))
    except EOFError:
        pass
    return frames

def playGifForDay(day):
    global frames, frameCount, currentFrame

    timelineGrid()

    gifPath = f"day{day}_{ageGroup}_{vaccineStatus}.gif"
    try:
        loadGif(gifPath)
        frameCount = len(frames)
        currentFrame = 0
        if frameCount == 0:
                print (f"No frames in {gifPath}")
                root.after(100, advanceDay)
                root.after(200, tickStep)
        else:
            showFrame()
    except Exception as e:
        print(f"Error loading {gifPath}: {e}")
        root.after(100, advanceDay)
        root.after(200, tickStep)

def showFrame():
    global currentFrame, isPlaying

    if not isPlaying:
        return

    if not frames:
            tickStep()
            return

    if currentFrame < frameCount:
        frame = frames[currentFrame]
        rightUpperRightCanvas.delete("all")
        rightUpperRightCanvas.image = frame
        rightUpperRightCanvas.create_image(0,0, anchor = "nw", image = frame)
        currentFrame += 1
        root.after(frameDelay, showFrame)
    else:
        advanceDay()
        tickStep()

def continueSimulation():
    if isPlaying:
        playGifForDay(ticker)

def advanceDay():
    global ticker

    if ticker > dayCount:
        timelineRunning = False
        button3.config(text = "Start Sim")
        return

    yValue = random.randint(40, 120) #change this once we get actual values
    dataPoints.append((ticker, yValue))

    displayNum.config(state = "normal")
    displayNum.insert("end", f"Day {ticker}: y = {yValue}\n")
    displayNum.see("end")
    displayNum.config(state = "disabled")

    timelineGrid()

    ticker += 1
    clockLabel.config(text = f"Day: {ticker}")
    
def tickStep(): #clock moment
    global isPlaying
    
    if isPlaying:
        if ticker <= dayCount:
            playGifForDay(ticker)
        else:
            isPlaying = False
            button3.config(text = "Start Sim")


def toggleSimulation(): #makes it so you can pause the sim
    global isPlaying, ageGroup, vaccineStatus
    
    if not isPlaying:
        ageGroup = button1Var.get()
        vaccineStatus = button2Var.get()

    isPlaying = not isPlaying
    button3.config(text = "pause sim" if isPlaying else "resume sim")

    if isPlaying:
        playGifForDay(ticker)

def resetSimulation(): #makes it so you can reset the sim
    global ticker, dataPoints, isPlaying

    isPlaying = False
    ticker = 0 
    dataPoints.clear()

    clockLabel.config(text = f"Day: {ticker}")
    button3.config(text = "Start Sim")

    timelineGrid()

    displayNum.config(state = "normal")
    displayNum.delete("1.0", "end")
    displayNum.insert("end", "values: \n")
    displayNum.config(state = "disabled")
    rightUpperRightCanvas.delete("all")

#button configs
button3.config(command = toggleSimulation)
button4.config(command = resetSimulation)

#actually make the thing go
timelineCanvas.bind("<Configure>", timelineGrid)
root.after(100, timelineGrid)
root.mainloop()
