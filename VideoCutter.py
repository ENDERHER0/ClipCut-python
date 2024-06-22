import os
from pytube import YouTube
from moviepy.editor import *
#Ask User for youtube url
url = input("Input URL: ")
fileName = input("Name for clip file: ")
videoMaxLength = float(input("Time in seconds for clip max length: "))
if not os.path.exists(fileName):os.mkdir("YoutubeDownloads/" + fileName)
yt = YouTube(url)
#format
mp4_files = yt.streams.filter(file_extension="mp4")
print("Format: MP4")
mp4_720p_files = mp4_files.get_by_resolution("720p")
print("Resolution: 720p")
latestDownload = mp4_720p_files.download("YoutubeDownloads")
#Get video ready for cutting
clip = VideoFileClip(latestDownload)
audio = AudioFileClip(latestDownload)
duration = float(clip.duration)
print("Duration: " + str(duration))
clipMaxDuration = videoMaxLength
clipDuration = 0
cut = 0
#Cut the video if its longer than 65 seconds
while(duration >= clipMaxDuration) :
    if(duration < videoMaxLength*2) & (duration > videoMaxLength):
        cut += 1
        extraCut = int(duration)
        break
    duration -= clipMaxDuration
    cut += 1 
print("Total Clips: " + str(cut))
print("Extra Video: " + str(extraCut))
#Cut and Save each clip
for i in range(cut):
    newClip = clip
    newAudio = audio
    print("Cutting Video")
    if(i < cut - 1) :
        newClip = newClip.subclip(clipDuration, clipMaxDuration)
        newAudio = newAudio.subclip(clipDuration, clipMaxDuration)
        newAudio.cutout(newClip.duration, newAudio.duration)
    else:
        newClip = newClip.subclip(clipDuration, clipDuration + extraCut)
        newAudio = newAudio.subclip(clipDuration, clipDuration + extraCut)
        newAudio.cutout(extraCut, newAudio.duration)
    newClip.write_videofile("YoutubeDownloads/" + fileName + "/Clip_" + str(i + 1) + ".mp4")
    print("Video: " + str(i + 1) + " Saved")
    clipDuration += videoMaxLength
    clipMaxDuration += videoMaxLength
input("Process Completed")