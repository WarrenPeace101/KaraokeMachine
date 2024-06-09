from urllib.request import Request, urlopen
import urllib
import requests
import urllib
from colorama import Fore, Style
import time
import coverpy
import climage
from PIL import Image
import musicbrainzngs

def printSongLyrics(response_body):
    lyrics = response_body.decode("utf-8")
    lyrics = lyrics.split("\\n")
    lyrics[len(lyrics) - 1] = lyrics[len(lyrics) - 1][:-2] #cuts off the last 2 letters of the final line

    print(Fore.BLUE + Style.BRIGHT)
    for lineNum in range(0, len(lyrics)):
        time.sleep(1.5)
        if len(lyrics[lineNum]) > 0:
            if lyrics[lineNum][-2] == "\\":
                lyrics[lineNum] = lyrics[lineNum][:-2]
        print(lyrics[lineNum])
    print("--------------------------------------------------")
    print(Fore.WHITE + Style.NORMAL)

    
def playSong():
    print(Fore.BLUE + Style.BRIGHT + "Enter the name of an artist:" + Fore.WHITE + Style.NORMAL)
    artistName = input()
    print(Fore.BLUE + Style.BRIGHT + f"Enter {artistName}'s song title: " + Fore.WHITE + Style.NORMAL)
    songTitle = input()

    print(Fore.BLUE + Style.BRIGHT + "--------------------------------------------------")

    # musicbrainzngs.set_useragent("KaraokeMachine", "0.0.1")
    # result = musicbrainzngs.search_artists(artist=artistName)
    # artistID = result["artist-list"][0]['id']

    # result = musicbrainzngs.search_recordings(artist = artistName, recording = songTitle)
    # songID = result["recording-list"][0]['id']
    # print(songID)

    # albumArt = musicbrainzngs.get_image("074e47eb-a1ad-450b-a784-f2915d5cbbe8", "front", "250", "release")
    # time.sleep(3)
    # img = Image.open(albumArt)
    # img.show()
    # r = requests.get("https://braze-images.com/appboy/communication/marketing/slide_up/slide_up_message_parameters/images/664f6e58d0d9f20059e19a83/09636775455cd06bdbe3a5581f034eb34a3322e5/original.png?1716481627", "myImage.png")
    # with open('myImg', 'wb') as outfile:
    #     outfile.write(r.content)
    #print(binary)
    # myCoverpy = coverpy.CoverPy()
    # result = myCoverpy.get_cover("Trench", 1)
    # with Image.open(result.artwork(100)) as img:
    #     img.show()
    # print(result.name)
    #print(result.artwork(100))
    #cover = climage.convert("nora.png")
    #print(cover)

    print(f"Now playing {songTitle} by {artistName}")
    print()

    if " " in artistName:
        artistName = artistName.replace(" ", "%20") #used to utilize the api
    if " " in songTitle:
        songTitle = songTitle.replace(" ", "%20") #used to utilize the api

    request = Request(f'https://api.lyrics.ovh/v1/{artistName}/{songTitle}')
    # if request.data == None:
    #     print(Fore.BLUE + Style.BRIGHT + "Song not found, try again!" + Fore.WHITE + Style.NORMAL)
    #     return None
    
    # startTime = time.time()
    try:
        response_body = urlopen(request, timeout = 3).read()
    except TimeoutError:
        print(Fore.BLUE + Style.BRIGHT + "Song not found, try again!" + Fore.WHITE + Style.NORMAL)
        return None


    printSongLyrics(response_body)

    artistName = artistName.replace("%20", " ") #swaps back to a cleaner name
    songTitle = songTitle.replace("%20", " ")
    
    return artistName, songTitle