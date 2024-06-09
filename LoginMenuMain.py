import os
from colorama import Fore, Style
import LoginMenuHelpers
import SharedMenuHelpers
import redis
import redisLogin
import musicbrainzngs

def loginMain(user, redisClient, mongoDatabase):
    #os.system('cls||clear')
    os.system('color 3f')
    print(Fore.BLUE + Style.BRIGHT + f"logged in as {user}"+ Fore.WHITE + Style.NORMAL)

    musicbrainzngs.set_useragent("KaraokeMachine", "0.0.1")

    # r = redis.Redis(
    # host= redisLogin.REDIS_HOST,
    # port= redisLogin.REDIS_PORT,
    # password=redisLogin.REDIS_PASS)

    #TO DO Mongo login

    menuOption = ""
    while menuOption != "logout":
        print(Fore.BLUE + Style.BRIGHT + "Enter command. Type 'help' for help:" + Fore.WHITE + Style.NORMAL)
        menuOption = input()
        match menuOption:
            case "logout":
                return
            case "karaoke":
                artistName, songTitle = SharedMenuHelpers.playSong()
                if artistName != None:
                    LoginMenuHelpers.addListenCount(user, artistName, songTitle, redisClient, mongoDatabase)
            case "help":
                LoginMenuHelpers.displayHelp()
            case "review":
                LoginMenuHelpers.createReview(user, redisClient, mongoDatabase)
            case "favorites":
                LoginMenuHelpers.listFavorites(user, redisClient, mongoDatabase)
            case "suggest":
                LoginMenuHelpers.suggestSong(user, redisClient, mongoDatabase)
            case "suggestions":
                LoginMenuHelpers.readSuggestions(user, redisClient, mongoDatabase)
            case "library":
                LoginMenuHelpers.listReviews(user, redisClient, mongoDatabase)
            case "_":
                print(Fore.BLUE + Style.BRIGHT + "Invalid command, type 'help' for help" + Fore.WHITE + Style.NORMAL)