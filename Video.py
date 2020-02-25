from pytube import YouTube
from pytube.exceptions import LiveStreamError, VideoUnavailable
import requests
import sys
from urllib.error import HTTPError

class Video:
    """Extractor let's you get video data from youtube url, and gives video resolution and sound quality lists for the requested video."""

    
    resolutionList = [] #List containing all available resolutions
    soundQualityList = [] #List containing all available sound quality level
    sizeInBytes = 0
    downloadedBytes = 0


    def downloadProgress(self, stream, chunk, bytes_remaining):

        self.downloadedBytes = self.sizeInBytes - bytes_remaining

        self.percentage = self.downloadedBytes / self.sizeInBytes * 100 #Calculating the percentage of download progress
        
        self.percentage = round(self.percentage, 1) #Rounding the percentage of progress to 1 decimal value

        print('{} %'.format(self.percentage)) #Displaying the percentage progress


    def downloadComplete(self, stream, file_path):

        print('Download Complete :)')
    

    def __init__(self, videoUrl):

        try:

            requests.get(videoUrl)  #Requesting video url to check internet connectivity
            
            self.video = YouTube(videoUrl, on_progress_callback = self.downloadProgress , on_complete_callback = self.downloadComplete)

            self.title = self.video.title #Extracting Video Tile

            self.description = self.video.description #Extracting Video Description

            self.thumbnailUrl= self.video.thumbnail_url #RExtracting Video Tumbnail Url 


            #Function the stores Video Resolutions in 'resolutionList' and Sond Quality in 'soundQualityLit' in ascending order

            for stream in self.video.streams:

                if (stream.resolution != None) and (stream.type == 'video') and (stream.audio_codec == 'mp4a.40.2'):

                    
                    if self.resolutionList.__contains__(stream.resolution): #Avoiding duplication of resolution values

                        continue

                    else:
                        
                        #Detecting if the stream is available to download
                        try:

                            stream.filesize

                            self.resolutionList.append(stream.resolution)

                        except HTTPError:

                            continue

                elif (stream.abr != None) and (stream.type == 'audio'):

                    if self.soundQualityList.__contains__(stream.abr): #Avoiding duplication of sound quality level

                        continue

                    else:

                        #Detecting if the stream is available to download
                        try:

                            stream.filesize

                            self.soundQualityList.append(stream.abr)

                        except HTTPError:

                            continue


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

        except LiveStreamError :

            print('This video is a live stram :(')

            sys.exit() #Terminating program

        except VideoUnavailable :

            print('The requested video is unavailable :(')

            sys.exit()

        except requests.ConnectionError: #Exception for no internet connectivity

            print('No or slow internet connection :(')

            sys.exit()


    def downloadVideo(self, resolution): #Function to download video by taking resolution as input

        try:

            #Sotring video size to track download progress
            self.sizeInBytes = self.video.streams.filter( audio_codec= 'mp4a.40.2' , res = resolution ).first().filesize

            #Initiating download
            self.video.streams.filter( audio_codec= 'mp4a.40.2' , res = resolution ).first().download()

        except requests.ConnectionError :

            print('No or slow internet connection :(')



    def downloadAudio(self, soundQuality): #Function to download video by taking resolution as input

        try:   

            #Sotring video size to track download progress
            self.sizeInBytes = self.video.streams.filter(abr= soundQuality).first().filesize

            #Initiating download
            self.video.streams.filter(abr = soundQuality).first().download()

        except requests.ConnectionError :

            print('No or slow internet connection :(')

        
        



    




