This is a working prototype. 

Instructions: 

1. Clone this repo

2. If your video does not have subtitles, or if it does but they are not contained in a separate file (i.e .ass or .srt), place your video(s) in this folder. If you have a show, or a collection of videos arranged in a specific way within a folder, you can put the entire folder structure in this folder and it will be preserved after encoding within the .mp4 folder. 
	2.a Double click the 000001.py script and let it run. 

3. If your video has subtitles contained in separate files, double click the 00002.py script. It will prompt you to select a video, and then the corresponding subtitle files. This script is more laborious in that you'll have to encode each video separately but hey, it's a WIP. 

4. After encoding, check to see if the videos are in the .mp4 folder. At this stage you can either double click the format errors.py file or manually see if the videos play in iTunes. It should be noted that sometimes format errors.py will flag a video as incompatible with iTunes despite it being compatible, and vice versa. 80% of the time it works 60% of the time.... Personally I'd check each file manually. 

5. If a video does not play in iTunes, you can put it in the format error folder (or if you ran the format errors script that's where the files went) and try re-encoding it with either of the iTunes encoding scripts. Sometimes that works. 

6. Add metadata and enjoy your videos in iTunes. 

7. Some videos are still falling through the cracks in that the encoded result is not compatible with iTunes. Hopefully I'll be able to fix this as I learn more about video, audio, and subtitle codecs. 


