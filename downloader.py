#!/usr/bin/python3

"""

    Written by BDeliers
    16 april 2020

    Under Apache 2.0 License

    This script downloads Snapchat's memories pictures and videos.

    To use it, download your Snapchat personnal data from https://accounts.snapchat.com/accounts/downloadmydata
    Then, launch this script by specifiying path to downloaded and unpacked Snapchat data folder
    The script will run and download each file in a subfolder Downloads in working directory

    Example :
        ./downloader.py /home/john/Downloads/mydata~1234567891234

"""

# HTML parser
from bs4 import BeautifulSoup

# HTTP requests
import requests

# To change creation time and make directory
from os import utime, mkdir

# To manage dates
from datetime import datetime
from time import mktime

# Args
from sys import argv

# Open Snapchat data memories file, depending on args
try:
    file = open("{}/html/memories_history.html".format(argv[1]), "r")
    html = file.read()

except:
    print("Invalid path to Snapchat data folder: {}/html/memories_history.html".format(argv[1]))
    exit()

# Creates Downloaded directory if needed
try:
    mkdir("./Downloaded")
except:
    pass

# Parse html
soup = BeautifulSoup(html, "html.parser")

# Get the picture's table
table = soup.find_all("tbody")[0]

photos = []
subDict = {}
i = 0

# For each line
for line in table.find_all("tr"):
    i = 0
    # For each cell
    for col in line.find_all("td"):
        # First cell is date of creation
        if i == 0:
            subDict["date"] = col.string
        # Second cell is type (PHOTO or VIDEO)
        elif i == 1:
            subDict["type"] = col.string
        # Third is a link to the download url
        elif i == 2:
            href = col.find("a").get("href")
            subDict["href"] = href[29:-3]

        i += 1

    # Store this data to the list
    photos.append(subDict)
    subDict = {}

# Remove first empty dict
photos.remove({})

# For each photos data
for photo in photos:
    print("Next !")

    # Get the file url
    r = requests.post(photo["href"], headers={"Content-type":"application/x-www-form-urlencoded"})
    photo["download"] = r.text

    # Download the photo
    r = requests.get(photo["download"])

    # Get its creation time to timestamp
    time = datetime.strptime(photo["date"], "%Y-%m-%d %H:%M:%S %Z")
    modTime = mktime(time.timetuple())

    # Name the downloaded file
    name = "Snapchat-{}".format((photo["date"].replace(' ', '@'))[:-4])

    # Give it an extension
    if photo["type"] == "PHOTO":
        name += ".jpg"
    elif photo["type"] == "VIDEO":
        name += ".mp4"

    # Store it to hard drive
    open("./Downloaded/{}".format(name), "wb").write(r.content)

    # Change its creation time
    utime("./Downloaded/{}".format(name), (modTime, modTime))
