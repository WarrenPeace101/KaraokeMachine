from colorama import Fore, Style
import musicbrainzngs

def displayHelp():
    print(Fore.BLUE + Style.BRIGHT)
    print("logout - used to logout of your account")
    print("karaoke - used to play a song")
    print("help - display commands")
    print("review - used to leave a review for a song")
    print("library - used to show all of your reviews")
    print("favorites - used to list your favorite songs")
    print("suggest - used to send a song suggestion to a friend")
    print("suggestions - used to display your song suggestions")
    print(Fore.WHITE + Style.NORMAL)

def addListenCount(user, artistName, songTitle, redisClient, mongoDatabase):
    result = musicbrainzngs.search_recordings(artist = artistName, recording = songTitle)
    songID = result["recording-list"][0]['id']

    #maybe update redis as well?

    #update mongo database
    if mongoDatabase.StreamedSongs.count_documents({"user":user, "songID":songID}) == 0:
        mongoDatabase.StreamedSongs.insert_one({"user":user, "songID": songID, "songTitle":songTitle, "artistName":artistName, "streams":1})
    else:
        mongoDatabase.StreamedSongs.update_one({"user":user, "songID": songID}, {"$inc":{"streams":1}})
    return

def createReview(user, redisClient, mongoDatabase):
    print(Fore.BLUE + Style.BRIGHT + "Enter the artist name to review:" + Fore.WHITE + Style.NORMAL)
    artistName = input()
    print(Fore.BLUE + Style.BRIGHT + f"Enter {artistName}'s song to review:" + Fore.WHITE + Style.NORMAL)
    songTitle = input()
    print(Fore.BLUE + Style.BRIGHT + "Please leave a review (less then 1000 characters):" + Fore.WHITE + Style.NORMAL)
    review = input()
    print(Fore.BLUE + Style.BRIGHT + "Please rate the song 0-100:" + Fore.WHITE + Style.NORMAL)
    rating = input()

    result = musicbrainzngs.search_recordings(artist = artistName, recording = songTitle)
    songID = result["recording-list"][0]['id']

    #put into redis if a favorite song
    #if rating > 80:
     #   redisClient.hset("Reviews", (artistName, songTitle), (review, rating)) #how do you check the key?

    #TO DO: insert review / rating into mongo
    mongoDatabase.SongReviews.insert_one({"user":user, "songID":songID, "songTitle":songTitle, "artistName":artistName, "review":review, "rating":rating})

def listReviews(user, redisClient, mongoDatabase):
    reviews = mongoDatabase.SongReviews.find({"user": user}, {"_id":0, "songTitle":1, "artistName": 1, "review":1, "rating":1})
    reviews = list(reviews)


    print(Fore.BLUE + Style.BRIGHT + "Reviews".center(130) + Fore.WHITE + Style.NORMAL)
    for review in reviews:
        print(Fore.BLUE + Style.BRIGHT + review["songTitle"].rjust(25) + " by " + review["artistName"] + review["review"].rjust(40) + " Rating: ".rjust(15) + review["rating"] + Fore.WHITE + Style.NORMAL)
    print()

def listFavorites(user, redisClient, mongoDatabase):
    print(Fore.BLUE + Style.BRIGHT + "How many of your top songs would you like to see?" + Fore.WHITE + Style.NORMAL)
    numOfSongs = input()
    numOfSongs = int(numOfSongs)
    # if numOfSongs <= 5: #only the top 5 songs are stored in the cache at a time!
    #     for songNum in range(len(numOfSongs)):
    #         print(redisClient.hget("Favorites", songNum))
            
    #access database, display top num

    topSongs = mongoDatabase.SongReviews.find({"user":user},{"_id":0, "songTitle":1, "artistName":1, "review":1, "rating":1}).sort({"rating":-1}).limit(numOfSongs)
    topSongs = list(topSongs)

    streams = []
    for songNum in range(len(topSongs)):
        numOfStreams = mongoDatabase.StreamedSongs.find({"user":user, "songTitle": topSongs[songNum]["songTitle"], "artistName":topSongs[songNum]["artistName"]}, {"_id":0, "streams":1})
        numOfStreams = list(numOfStreams)
        if len(numOfStreams) > 0:
            streams.append(str(numOfStreams[0]["streams"]))
        else:
            streams.append("0")


    print(Fore.BLUE + Style.BRIGHT + "Favorite Songs".center(130) + Fore.WHITE + Style.NORMAL)
    for topSongNum in range(len(topSongs)):
        print(Fore.BLUE + Style.BRIGHT + topSongs[topSongNum]["songTitle"].rjust(25) + " by " + topSongs[topSongNum]["artistName"] + ": " + topSongs[topSongNum]["review"].rjust(40) + " Rating: ".rjust(15) + topSongs[topSongNum]["rating"] + "Streams: ".rjust(15) + streams[topSongNum] + Fore.WHITE + Style.NORMAL)
    print()

def listStats():
    #display most played song, favorite artist, list of reviews

    return

def suggestSong(user, redisClient, mongoDatabase):
    print(Fore.BLUE + Style.BRIGHT + "What song would you like to recommend?" + Fore.WHITE + Style.NORMAL)
    songTitle = input()
    print(Fore.BLUE + Style.BRIGHT + "Who is the artist of this song?" + Fore.WHITE + Style.NORMAL)
    artistName = input()
    print(Fore.BLUE + Style.BRIGHT + "Who are you recommending this song to? (Enter their username)" + Fore.WHITE + Style.NORMAL)
    friendUsername = input()

    result = musicbrainzngs.search_recordings(artist = artistName, recording = songTitle)
    songID = result["recording-list"][0]['id']

    mongoDatabase.SuggestedSongs.insert_one({"sendingUser":user, "receivingUser":friendUsername, "songID":songID, "songTitle":songTitle, "artistName":artistName})
    print("Suggestion sent!")                                       


def readSuggestions(user, redisClient, mongoDatabase): 
    print(Fore.BLUE + Style.BRIGHT + "Song suggestions".center(140) + Fore.WHITE + Style.NORMAL)

    songSuggestions = mongoDatabase.SuggestedSongs.find({"receivingUser": user}, {"_id":0, "sendingUser":1, "songTitle":1, "artistName": 1})
    songSuggestions = list(songSuggestions)

    for songSuggestion in songSuggestions:
        print(Fore.BLUE + Style.BRIGHT + songSuggestion["sendingUser"].rjust(40) + " suggested you listen to " + songSuggestion["songTitle"] + " by " + songSuggestion["artistName"] + Fore.WHITE + Style.NORMAL)






