import tkinter as tk
from PIL import Image, ImageTk
import random

root = tk.Tk()
root.title("gifTester")
root.geometry("1200x800")

gifWidth = 300
gifHeight = 300

sidePanel = tk.Frame(root, width = 200, bg = "white")
sidePanel.pack(side = tk.LEFT, fill = tk.Y)

buttonFrame = tk.Frame(sidePanel, bg = "white")
buttonFrame.pack(pady = 20)

pauseButton = tk.Button(buttonFrame, text = "Pause", command = lambda: pause())
pauseButton.pack(side = tk.LEFT, padx = 10)

playButton = tk.Button(buttonFrame, text = "Resume", command = lambda: resume())
playButton.pack(side = tk.LEFT, padx = 10)

mainPanel = tk.Frame(root)
mainPanel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frameCounter = tk.Label(root, text = "Frame: 0/0")
frameCounter.pack()

label = tk.Label(root)
label.pack(expand = True)

timelinePanel = tk.Frame(root, bg = "white")
timelinePanel.pack(side = tk.BOTTOM, fill = tk.X)

timelineFrame = tk.Frame(timelinePanel, bg = "white")
timelineFrame.pack(padx = 10, pady = 10, fill = tk.X)

timelineLabel = tk.Label(timelineFrame, text = "Timeline:", bg = "white")
timelineLabel.pack(side = tk.LEFT)

timelineList = tk.Listbox(timelineFrame, height = 5)
timelineList.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = 10)

gifPath = ["day1.gif", "day2.gif"]
currentGif = 0

frames = []
frameCount = 0
currentFrame = 0
frameDelay = 50 
isPlaying = True
dayCount = 0

def loadGif(path):
    global frames, frameCount
    frames = []
    img = Image.open(path)

    try:
        while True:
            frame = img.copy().convert("RGBA")
            frame = frame.resize((gifWidth, gifHeight), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            img.seek(len(frames))
    except EOFError:
        pass

    frameCount = len(frames)

print(f"total frames: {frameCount}")

def updateFrame():
    global currentFrame, currentGif
    
    if isPlaying:
        label.config(image = frames[currentFrame])
        frameCounter.config(text = f"Frame: {currentFrame + 1}/{frameCount}")
        currentFrame += 1
        if currentFrame >= frameCount:
            currentGif = (currentGif + 1) % len(gifPath)
            loadGif(gifPath[currentGif])
            currentFrame = 0 

    root.after(frameDelay, updateFrame)

def pause():
    global isPlaying
    isPlaying = False

def resume():
    global isPlaying
    isPlaying = True

loadGif(gifPath[currentGif])
updateFrame()
root.mainloop()