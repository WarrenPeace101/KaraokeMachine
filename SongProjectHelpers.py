from urllib.request import Request, urlopen
import bcrypt

def displayHelp():
    print("create - creates a new user account")
    print("login - used to login to your account")
    print("quit - exit program")
    print("karaoke - used to play a song without logging in")
    print("help - display commands")

def printSongLyrics(response_body):
    lyrics = response_body.decode("utf-8")
    lyrics = lyrics.split("\\n")
    lyrics[len(lyrics) - 1] = lyrics[len(lyrics) - 1][:-2] #cuts off the last 2 letters of the final line

    for lineNum in range(1, len(lyrics)):
        print(lyrics[lineNum])

    
def playSong():
    print("Enter the name of an artist:")
    artistName = input()
    print(f"Enter {artistName}'s song title: ")
    songTitle = input()

    print(f"Now playing {songTitle} by {artistName}")
    print()

    if " " in artistName:
        artistName = artistName.replace(" ", "%20") #used to utilize the api
    if " " in songTitle:
        songTitle = songTitle.replace(" ", "%20") #used to utilize the api


    request = Request(f'https://api.lyrics.ovh/v1/{artistName}/{songTitle}')
    response_body = urlopen(request).read()

    printSongLyrics(response_body)


def createUser():
    print("Enter your username:")
    username = input()
    #TO DO:: check to see if the username is in your database somehow
    print("Enter password: ")
    passOne = input()
    print("Confirm password:")
    passTwo = input()
    if passOne != passTwo:
        print("oops, try again!")
        return
    passOneBytes = str.encode(passOne)
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(passOneBytes, salt)
    print(hashedPassword)


def loginUser():
    

        

    