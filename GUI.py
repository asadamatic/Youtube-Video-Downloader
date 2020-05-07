from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter.messagebox import showerror , showinfo
from PIL import Image , ImageTk
from urllib.request import urlopen
from io import BytesIO
from Video import Video
import os
from threading import Thread



"""Creating window for the downloader and configuring basic settings"""
rootWindow =  Tk()
rootWindow.title('YouTube Video Downlader')
rootWindow.resizable(0, 0)
rootWindow.iconbitmap(r'D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\windowIcon.ico')

def disableFrameExceptProgressBar(frame):

    for child in frame.winfo_children():
        if type(child) == Message or type(child) == Progressbar or type(child) == Label or type(child) == Frame:
            pass
        else:
            child.config(state = DISABLED)

def disableFrameExceptLabel(frame):

    for child in frame.winfo_children():
        if type(child) == Message or type(child) == Progressbar or type(child) == Label or type(child) == Frame:
            pass
        else:
            child.config(state = DISABLED)

def enableFrame(frame):

    for child in frame.winfo_children():
        if type(child) == Message or type(child) == Progressbar or type(child) == Label or type(child) == Frame:
            pass
        else:
            child.config(state = NORMAL)

#Frame that contains all the elements of the User Interface
mainFrame = Frame(rootWindow, height = 700 , width = 900 , relief = SUNKEN , bg = '#ffffff')
mainFrame.pack()

#Loading Logo Image
logoImage = Image.open(r"D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\logo.png")
logo = ImageTk.PhotoImage(logoImage)

#Loading video Thumbnail and creating photoImage
thumbnailImage = Image.open(r"D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\thumbnail.png")
dummyThumbnail = ImageTk.PhotoImage(thumbnailImage)

logoDisplay = Label(mainFrame , image = logo , bg = '#ffffff')
logoDisplay.place(x = 370 , y = 60)

videoUrl = StringVar()
videoUrlInput = Entry(mainFrame, width = 40 , fg = '#707070' ,  font = ('Aerial', 18) , textvariable = videoUrl , relief = FLAT ,  borderwidth = 4 , highlightthickness=4 , highlightcolor="#CCCCCC")
videoUrlInput.place(x = 50, y = 250)

#Displaying placeholder text
videoUrlInput.insert(0 , 'Paste video url here...')

def downloadProgress(stream, chunk, bytes_remaining):

        downloadedBytes = video.sizeInBytes - bytes_remaining
        percentage = downloadedBytes / video.sizeInBytes * 100 #Calculating the percentage of download progress
        progressBar['value'] = percentage
        mainFrame.update_idletasks()

def downloadComplete(stream, file_path):

        loadingMessage.set('Download Complete')
        progressBar.place_forget()
        downloadButton.place_forget()
        formatSelector.place_forget()
        resolutionSelector.place_forget()
        enableFrame(mainFrame)

"""#Initiating search for file formats and resolutions once the user presses 'Search' button"""
def startSearching(url):

    loadingMessage.set('Wait while preview video is being Loaded.....')
    title.set('Video title will appear here...')

    disableFrameExceptLabel(mainFrame)
    videoTumbnail.configure(image = dummyThumbnail)
    global video
    video = Video(url , downloadProgress , downloadComplete)
    enableFrame(mainFrame)

    if video.errorMessage == '':

        searchVideo.config(state = DISABLED)
        title.set(video.title)

        #openning thumbnail url and downloading thumbnail
        openThumbnailUrl = urlopen(video.thumbnailUrl)
        readThumbnail = openThumbnailUrl.read()
        openThumbnailUrl.close()

        #creating Thumbnail image out of thumbnail data loaded from the url
        thumbnailImage = Image.open(BytesIO(readThumbnail))
        thumbnailImage = thumbnailImage.resize((246 , 138) , Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(thumbnailImage)
        videoTumbnail.configure(image = thumbnail)
        videoTumbnail.image = thumbnail

        global fileResolution
        fileResolution = StringVar(mainFrame)
        fileResolution.set(video.resolutionList[0])
        
        #Providing resolution options to the user
        global resolutionSelector
        resolutionSelector = OptionMenu(mainFrame , fileResolution , *video.resolutionList)
        resolutionSelector.place(x = 800, y = 260)
        
        #File formats available to download
        formats = ['Video' , 'Audio']

        global fileFormat
        fileFormat = StringVar()
        fileFormat.set(formats[0])
        
        #Providing format options to the user 
        global formatSelector
        formatSelector = OptionMenu(mainFrame , fileFormat, *formats , command = siwtchFormat)
        formatSelector.place(x = 700, y = 260)
        
        formatSelector.config(font = ('Aerial' , 12) , relief = FLAT) 
        resolutionSelector.config( font = ('Aerial' , 12) , relief = FLAT)
        searchVideo.config(state = NORMAL)
        downloadButton.place(x = 50 , y = 400)
        downloadButton.focus()
        loadingMessage.set('')

    else:

        showerror('Error Occured' , video.errorMessage)
        loadingMessage.set('')

def siwtchFormat(value):

    if fileFormat.get() == 'Video':
        resolutionSelector['menu'].delete(0 , 'end')
        fileResolution.set(video.resolutionList[0])

        for item in video.resolutionList:
            resolutionSelector['menu'].add_command(label = item , command = lambda value = item : fileResolution.set(value)) 


    elif fileFormat.get() == 'Audio':
        resolutionSelector['menu'].delete(0 , 'end')
        fileResolution.set(video.soundQualityList[0])

        for item in video.soundQualityList:
            resolutionSelector['menu'].add_command(label = item , command = lambda value = item : fileResolution.set(value))


def startDownload(dummyArgument):

    progressBar.focus()
    disableFrameExceptProgressBar(mainFrame)
    progressBar.place(x = 300 , y = 400)

    if fileFormat.get() == 'Video':
        video.downloadVideo(fileResolution.get())

    elif fileFormat.get() == 'Audio':
        video.downloadAudio(fileResolution.get())

def extractVideoThread():
    
    Thread(target= startSearching, args = (videoUrl.get(),)).start()
    
def startDownloadThread():

    Thread(target= startDownload, args = (1,)).start()

searchVideo = Button(mainFrame ,  font = ('Aerial' , 14) , text = 'Search' , relief = FLAT , command = extractVideoThread , highlightthickness=4 , highlightcolor="#CCCCCC" )
searchVideo.place(x = 600 , y = 250)

loadingMessage = StringVar()
loadingMessage.set('')
LoadingVideo = Label(mainFrame , font = ('Aerial' , 12) , textvariable = loadingMessage, bg = '#ffffff')
LoadingVideo.place(x = 390 , y = 370)

downloadButton = Button(mainFrame ,  font = ('Aerial' , 14) , text = 'Start Downlaod' , relief = FLAT , command = startDownloadThread , highlightthickness= 4 , highlightcolor="#CCCCCC")

progressBar = Progressbar(mainFrame , length = 300 , orient = HORIZONTAL , mode = 'determinate')

videoPreview = Frame(mainFrame , height = 160 , width = 800)
videoPreview.place(x = 50 , y = 500)

videoTumbnail = Label(mainFrame , height = 138 , width = 246 , image = dummyThumbnail )
videoTumbnail.place(x = 60 , y = 510)


title = StringVar()
title.set('Video title will appear here...')
vidoTitle = Message(mainFrame , width = 530 , textvariable = title , font = ('Aerial' , 13) , fg = '#0D0D0D')
vidoTitle.place(x = 330 , y = 510)


"""Functions for events binded to widgets"""

#Removing placeholder from videoUrl box on click
def eraseText(event):

    if videoUrl.get() == 'Paste video url here...':
        videoUrl.set('')


"""#Binding events to wdgets"""
videoUrlInput.bind('<Button-1>' , eraseText)

rootWindow.mainloop()