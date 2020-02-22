from pytube import YouTube

class Video:
    """Extractor let's you get video data from youtube url, and gives video resolution and sound quality lists for the requested video."""

    
    resolutionList = [] #List containing all available resolutions
    soundQualityList = [] #List containing all available sound quality level
    sizeInBytes = 0
    downloadedBytes = 0


    def downloadProgress(self, stream, chunk, bytes_remaining):

        self.downloadedBytes = self.sizeInBytes - bytes_remaining

        self.percentage = self.downloadedBytes / self.sizeInBytes * 100
        self.percentage = round(self.percentage, 1)
        print('{} %'.format(self.percentage))


    def downloadComplete(self, stream, file_path):

        print('Download Complete :)')
    

    def __init__(self, videoUrl):

        self.video = YouTube(videoUrl, on_progress_callback = self.downloadProgress , on_complete_callback = self.downloadComplete)

        self.title = self.video.title #Extracting Video Tile

        self.description = self.video.description #Extracting Video Description

        self.thumbnailUrl= self.video.thumbnail_url #RExtracting Video Tumbnail Url 


        #Function the stores Video Resolutions in 'resolutionList' and Sond Quality in 'soundQualityLit' in ascending order

        for stream in self.video.streams:

            if (stream.resolution != None) and (stream.type == 'video'):

                
                if self.resolutionList.__contains__(stream.resolution): #Avoiding duplication of resolution values

                    continue

                else:

                    self.resolutionList.append(stream.resolution)

            elif (stream.abr != None) and (stream.type == 'audio'):

                if self.soundQualityList.__contains__(stream.abr): #Avoiding duplication of sound quality level

                    continue

                else:

                    self.soundQualityList.append(stream.abr)


        #Sorting video resolutions
        for resolution in range(len(self.resolutionList)):

            #Removing 'p' from resolutions and converting resolutions to integer
            self.resolutionList[resolution] = int(self.resolutionList[resolution].replace('p', ''))



        self.resolutionList.sort() 

        for resolution in range(len(self.resolutionList)):

            #Converting the array into original resolution format
            self.resolutionList[resolution] = str(self.resolutionList[resolution]) + 'p'

            

        for soundQuality in range(len(self.soundQualityList)):

            #Removing 'kbps' from resolutions and converting resolutions to integer
            self.soundQualityList[soundQuality] = int(self.soundQualityList[soundQuality].replace('kbps', ''))


        self.soundQualityList.sort()

        for soundQuality in range(len(self.soundQualityList)):

            #Removing 'kbps' from resolutions and converting resolutions to integer
            self.soundQualityList[soundQuality] = str(self.soundQualityList[soundQuality]) + 'kbps'

    def downloadVideo(self, resolution): #Function to download video by taking resolution as input

        self.sizeInBytes = self.video.streams.filter(only_video= True , res = resolution).first().filesize

        self.video.streams.filter(only_video= True , res = resolution).first().download()


    def downloadAudio(self, soundQuality): #Function to download video by taking resolution as input

        self.sizeInBytes = self.video.streams.filter(only_audio = True , abr= soundQuality).first().filesize

        self.video.streams.filter(only_audio = True , abr = soundQuality).first().download()

        
        



    




