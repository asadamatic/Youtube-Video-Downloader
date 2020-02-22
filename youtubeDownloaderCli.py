from Video import Video

videoUrl = input('Enter video URL: ')

video = Video(videoUrl)


print(video.title)
print(video.description)


formatChoice = input('Choose a file format (Press 1 or 2), \n 1. Video \n 2. Audio \n')
formatChoice = int(formatChoice)


if formatChoice == 1:

    print('Choose a resolution for your Video: ')
    for resolution in range(len(video.resolutionList)):

        print(resolution  + 1, video.resolutionList[resolution], sep= '    ')

    resolutionChoice = input('Choose corresponding number to select: ')
    resolutionChoice = int(resolutionChoice) - 1
    
    video.downloadVideo(video.resolutionList[resolutionChoice])

    
elif formatChoice == 2:
    
    print('Choose a quality for your Audio: ')
    for soundQuality in range(len(video.soundQualityList)):

        print(soundQuality + 1, video.soundQualityList[soundQuality], sep= '    ')

    qualityChoice = input('Choose corresponding number to select: ')

    qualityChoice = int(qualityChoice) - 1

    video.downloadAudio(video.soundQualityList[qualityChoice])
   

else:

    print('Choose from the given options :)')



