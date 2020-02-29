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
rootWindow.iconbitmap(r'D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\windowIcon.ico')


#Frame that contains all the elements of the User Interface
mainFrame = Frame(rootWindow, height = 700 , width = 900 , relief = SUNKEN , bg = '#ffffff')
mainFrame.pack()

#Loading Logo Image
logoImage = Image.open(r"D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\logo.png")
logo = ImageTk.PhotoImage(logoImage)

#Loading video Thumbnail and creating photoImage
thumbnailImage = Image.open(r"D:\Python Projects\GitHub\YouTube Downloader\Video Downloader\Assets\thumbnail.png")
thumbnail = ImageTk.PhotoImage(thumbnailImage)


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

        showinfo('Download Complete')

        progressBar.place_forget()
        downloadButton.place_forget()
        formatSelector.place_forget()
        resolutionSelector.place_forget()
        
        searchVideo.config(state = NORMAL)
        changePath.config(state = NORMAL)

    

"""#Initiating search for file formats and resolutions once the user presses 'Search' button"""
def startSearching():

    LoadingVideo.place(x = 390 , y = 370)

    global video

    video = Video(videoUrl.get() , downloadProgress , downloadComplete)

    if video.errorMessage == '':

        searchVideo.config(state = DISABLED)
        changePath.config(state = DISABLED)

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
        changePath.config(state = NORMAL)

        downloadButton.place(x = 50 , y = 400)

        videoUrlInput.delete(0 , 'end')

        downloadButton.focus()

        LoadingVideo.place_forget()

    else:

        showerror('Error Occured' , video.errorMessage)

        LoadingVideo.place_forget()


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


def startDownload():

    progressBar.focus()

    searchVideo.config(state = DISABLED)
    formatSelector.config(state = DISABLED)
    resolutionSelector.config(state = DISABLED)
    downloadButton.config(state = DISABLED)
    changePath.config(state = DISABLED)

    progressBar.place(x = 300 , y = 400)

    if fileFormat.get() == 'Video':

        video.downloadVideo(fileResolution.get())

    elif fileFormat.get() == 'Audio':

        video.downloadAudio(fileResolution.get())

 
startSearchingThread = Thread(target= startSearching)
downloadVideoThread = Thread(target= startDownload)


def extractVideoThread():
   
    startSearchingThread.start()
    

def startDownloadThread():

    downloadVideoThread.start()


searchVideo = Button(mainFrame ,  font = ('Aerial' , 14) , text = 'Search' , relief = FLAT , command = extractVideoThread , highlightthickness=4 , highlightcolor="#CCCCCC" )
searchVideo.place(x = 600 , y = 250)


filePath = StringVar()
filePath.set(os.getcwd())
showPath = Entry(mainFrame, width = 40 , textvariable =  filePath ,  font = ('Aerial', 18) , relief = FLAT , state = DISABLED , borderwidth = 4 , highlightthickness=4 , highlightcolor="#CCCCCC")
showPath.place(x = 50, y = 320)

def changeDownloadPath():

    filePath = filedialog.askdirectory()
    showPath.config(state = NORMAL)
    showPath.delete(0 , END)
    showPath.insert(0 , filePath)
    showPath.config(state = DISABLED)


changePath = Button(mainFrame ,  font = ('Aerial' , 14) , text = 'Change Path' , relief = FLAT ,  command = startDownloadThread ,  highlightthickness=4 , highlightcolor="#CCCCCC")
changePath.place(x = 600 , y = 320)

LoadingVideo = Label(mainFrame , font = ('Aerial' , 10) , text = 'Wait while video is being Loaded.....' , bg = '#ffffff')
LoadingVideo.place(x = 390 , y = 370)
LoadingVideo.place_forget()

downloadButton = Button(mainFrame ,  font = ('Aerial' , 14) , text = 'Start Downlaod' , relief = FLAT , command = startDownloadThread , highlightthickness= 4 , highlightcolor="#CCCCCC")
downloadButton.place(x = 50 , y = 400)
downloadButton.place_forget()

progressBar = Progressbar(mainFrame , length = 300 , orient = HORIZONTAL , mode = 'determinate')
progressBar.place(x = 300 , y = 400)
progressBar.place_forget()

videoPreview = Frame(mainFrame , height = 160 , width = 800)
videoPreview.place(x = 50 , y = 500)

videoTumbnail = Label(mainFrame , height = 138 , width = 246 , image = thumbnail )
videoTumbnail.place(x = 60 , y = 510)


title = StringVar()
title.set('Video title will appear here...')
vidoTitle = Message(mainFrame , width = 530 , textvariable = title , font = ('Aerial' , 13) , fg = '#0D0D0D')
vidoTitle.place(x = 330 , y = 510)


"""Functions for events binded to widgets"""

#Removing placeholder from videoUrl box on click
def eraseText(event):

    if videoUrl.get() == 'Paste video url here...':
        
        videoUrlInput.delete(0 , 'end')
        videoUrl.set('')


"""#Binding events to wdgets"""
videoUrlInput.bind('<Button-1>' , eraseText)

rootWindow.mainloop()