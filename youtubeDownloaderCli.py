from Video import Video

videoUrl = input('Enter video URL: ')

video = Video(videoUrl)


print(video.title)
print(video.description)

#Asking user to choose a format from Audion and Video to download
formatChoice = input('Choose a file format (Press 1 or 2), \n 1. Video \n 2. Audio \n')
formatChoice = int(formatChoice)


if formatChoice == 1:

    #Detecting if there are video resolutions available to download
    if len(video.resolutionList) == 0:

        print('Video is not avaiable to download :)')
    else:

        print('Choose a resolution for your Video: ')

        for resolution in range(len(video.resolutionList)):

            print(resolution  + 1, video.resolutionList[resolution], sep= '    ')

        #Asking the user to choose a resolution for the download
        resolutionChoice = input('Choose corresponding number to select: ')

        #Decrementing the user input to matach the list index
        resolutionChoice = int(resolutionChoice) - 1

        #Calling downloadVideo function from Video class to initialize video downloading
        video.downloadVideo(video.resolutionList[resolutionChoice])

    
elif formatChoice == 2:
    
    #Detecting if there are sound qualities available to download
    if len(video.soundQualityList) == 0:

        print('Video is not avaiable to download :)')
    else:
        
        print('Choose a quality for your Audio: ')

    
        for soundQuality in range(len(video.soundQualityList)):

            print(soundQuality + 1, video.soundQualityList[soundQuality], sep= '    ')

        #Asking the user to choose a resolution for the download
        qualityChoice = input('Choose corresponding number to select: ')

        #Decrementing the user input to matach the list index
        qualityChoice = int(qualityChoice) - 1
        
        #Calling downloadAudio function from Video class to initialize Audio downloading
        video.downloadAudio(video.soundQualityList[qualityChoice])
   

else:

    print('Choose from the given options :)')



