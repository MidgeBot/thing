import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import re

root = tk.Tk()
root.title("VariVirus")
root.geometry("1200x800")

# Variables
ticker = 0
maxDayCount = 17
currentImgIndex = 0
gridlinePositions = []
dataPoints = []
ageGroup = None
vaccineStatus = None
isPlaying = False

# Utility
def getPartNumber(filename):
    match = re.search(r"pt\.(\d+)", filename)
    return int(match.group(1)) if match else 0

# UI Layout
# Title
headerFrame = tk.Frame(root, height=50, bg='lightblue')
headerFrame.pack(fill='x')
headerLabel = tk.Label(headerFrame, text="VariVirus", bg='lightblue', font=("Arial", 16))
headerLabel.pack(pady=10)

# Main Panels
mainFrame = tk.Frame(root)
mainFrame.pack(fill="both", expand=True)

leftPanel = tk.Frame(mainFrame, width=150, bg="lightgrey")
leftPanel.pack(side="left", fill="y")

# Left Side Buttons
ageVar = tk.StringVar(value="Age group")
ageOptions = ["young", "old"]
tk.OptionMenu(leftPanel, ageVar, *ageOptions).pack(pady=10, padx=10, fill="x")

vaccineVar = tk.StringVar(value="Vaccinated")
vaccineOptions = ["yes", "No"]
tk.OptionMenu(leftPanel, vaccineVar, *vaccineOptions).pack(pady=10, padx=10, fill="x")

startPauseButton = tk.Button(leftPanel, text="Start Sim")
startPauseButton.pack(pady=10, padx=10, fill="x")

resetButton = tk.Button(leftPanel, text="Reset Sim")
resetButton.pack(pady=10, padx=10, fill="x")

clockLabel = tk.Label(leftPanel, text=f"Day: {ticker}", bg="black", fg="white", font=("Arial", 12))
clockLabel.pack(padx=10)

displayBox = tk.Text(leftPanel, height=20, width=20, font=("Arial", 12))
displayBox.pack(pady=10, padx=10, fill="x")
displayBox.insert("end", "values: \n")
displayBox.config(state="disabled")

# Right Panel
rightPanel = tk.Frame(mainFrame, bg="white", bd=1, relief="solid")
rightPanel.pack(side="right", fill="both", expand=True)

rightUpperBox = tk.Frame(rightPanel, bg="white", bd=1, relief="solid")
rightUpperBox.pack(fill="both", expand=True, padx=10, pady=(10, 5))

leftPane = tk.Frame(rightUpperBox, bg="white")
leftPane.pack(side="left", fill="both", expand=True)

rightPane = tk.Frame(rightUpperBox, bg="white")
rightPane.pack(side="left", fill="both", expand=True)

tk.Label(rightPane, text="Lymph", bg="lightblue", font=("Arial", 12)).pack(fill="x")
tk.Label(leftPane, text="Lungs", bg="lightblue", font=("Arial", 12)).pack(fill="x")

leftCanvas = tk.Canvas(leftPane, bg="white")
leftCanvas.pack(side="left", fill="both", expand=True)

rightCanvas = tk.Canvas(rightPane, bg="white")
rightCanvas.pack(side="left", fill="both", expand=True)

# Timeline Section
rightLowerBox = tk.Frame(rightPanel, height=200, bg="lightgrey", highlightbackground="black", highlightthickness=1)
rightLowerBox.pack(fill="x", padx=10, pady=(0, 10))

timelineCanvas = tk.Canvas(rightLowerBox, bg="white", height=200)
timelineCanvas.pack(fill="both", padx=5, pady=5)

# Draw timeline grid
def drawTimelineGrid(event=None):
    global gridlinePositions
    timelineCanvas.delete("all")
    width = timelineCanvas.winfo_width()
    spacing = width / maxDayCount
    gridlinePositions = [i * spacing for i in range(maxDayCount + 1)]

    for x in gridlinePositions:
        timelineCanvas.create_line(x, 0, x, 200, fill="lightblue")

    last = None
    r = 4
    for day, y in dataPoints:
        x = gridlinePositions[day]
        timelineCanvas.create_oval(x - r, y - r, x + r, y + r, fill="red")
        if last:
            timelineCanvas.create_line(last[0], last[1], x, y, fill="blue", width=2)
        last = (x, y)

def displayDayImages(day):
    leftDir = "images/left"
    rightDir = "images/right"

    leftImages = sorted(
        [os.path.join(leftDir, f) for f in os.listdir(leftDir) if f"Day {day} pt." in f],
        key=getPartNumber
    )
    rightImages = sorted(
        [os.path.join(rightDir, f) for f in os.listdir(rightDir) if f"Day {day} pt." in f],
        key=getPartNumber
    )

    if not leftImages and not rightImages:
        print(f"No images for Day {day}")
        advanceDay()
        return

    progress = {"left": False, "right": False}

    def checkAdvance():
        if progress["left"] and progress["right"]:
            advanceDay()

    def showSeries(canvas, imageList, side):
        def display(index):
            if index >= len(imageList):
                progress[side] = True
                checkAdvance()
                return

            if not isPlaying:
                root.after(200, lambda: display(index))
                return

            imgPath = imageList[index]
            try:
                img = Image.open(imgPath)
                w, h = canvas.winfo_width(), canvas.winfo_height()
                img = img.resize((w, h), Image.LANCZOS)
                tkImg = ImageTk.PhotoImage(img)
                canvas.delete("all")
                canvas.image_cache = [tkImg]
                canvas.create_image(0, 0, anchor="nw", image=tkImg)

                root.after(1000, lambda: display(index + 1))
            except Exception as e:
                print(f"Error loading {imgPath}: {e}")
                display(index + 1)

        display(0)

    showSeries(leftCanvas, leftImages, "left")
    showSeries(rightCanvas, rightImages, "right")

def tick():
    if isPlaying:
        displayDayImages(ticker)

def advanceDay():
    global ticker
    if ticker >= maxDayCount:
        startPauseButton.config(text="Start Sim")
        return

    y = random.randint(40, 120)
    dataPoints.append((ticker, y))

    displayBox.config(state="normal")
    displayBox.insert("end", f"Day {ticker}: y = {y}\n")
    displayBox.see("end")
    displayBox.config(state="disabled")

    drawTimelineGrid()
    ticker += 1
    clockLabel.config(text=f"Day: {ticker}")

    if isPlaying:
        root.after(1000, tick)

def toggleSim():
    global isPlaying, ageGroup, vaccineStatus
    if not isPlaying:
        ageGroup = ageVar.get()
        vaccineStatus = vaccineVar.get()

    isPlaying = not isPlaying
    startPauseButton.config(text="Pause Sim" if isPlaying else "Resume Sim")

    if isPlaying:
        displayDayImages(ticker)

def resetSim():
    global ticker, dataPoints, isPlaying
    ticker = 0
    dataPoints.clear()
    isPlaying = False

    clockLabel.config(text=f"Day: {ticker}")
    startPauseButton.config(text="Start Sim")

    drawTimelineGrid()

    displayBox.config(state="normal")
    displayBox.delete("1.0", "end")
    displayBox.insert("end", "values: \n")
    displayBox.config(state="disabled")

    leftCanvas.delete("all")
    rightCanvas.delete("all")

# Bindings and Commands
startPauseButton.config(command=toggleSim)
resetButton.config(command=resetSim)

timelineCanvas.bind("<Configure>", drawTimelineGrid)
leftCanvas.bind("<Configure>", lambda e: ticker > 0 and displayDayImages(ticker - 1))
rightCanvas.bind("<Configure>", lambda e: ticker > 0 and displayDayImages(ticker - 1))

root.after(100, drawTimelineGrid)
root.mainloop()
