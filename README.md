# Snapchat Memories Downloader

Python script that downloads all your Snapchat memories pictures and videos automatically !

Under Apache 2.0 License

### Written by BDeliers
#### 16 april 2020

# How to use ?

This script downloads Snapchat's memories pictures and videos.

To use it, download your Snapchat personnal data from [Snapchat's website](https://accounts.snapchat.com/accounts/downloadmydata)
Then, launch this script by specifiying path to downloaded and unpacked Snapchat data folder
The script will run and download each file in a subfolder Downloads in working directory

Since it dowloads all your memories, it can take a long time ! (yes, it's a possible improvement)

Example :
    ./downloader.py /home/john/Downloads/mydata~1234567891234
