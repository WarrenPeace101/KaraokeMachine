import os
from colorama import Fore, Style
import StartMenuHelpers
import LoginMenuMain
import SharedMenuHelpers
import redisLogin
import redis
import pymongo

#from urllib2 import Request, urlopen
redisClient = redis.Redis(
    host= redisLogin.REDIS_HOST,
    port= redisLogin.REDIS_PORT,
    password=redisLogin.REDIS_PASS)

#mongo
connectionURL = f"mongodb+srv://{redisLogin.MONGO_USER}:{redisLogin.MONGO_PASS}@songcluster.dmalyuk.mongodb.net/?retryWrites=true&w=majority&appName=SongCluster"
mongoClient = pymongo.mongo_client.MongoClient(connectionURL)
mongoDatabase = mongoClient.get_database("SongDatabase")
#print(f"Ping result: {mongoClient.admin.command('ping')}")

os.system('cls||clear')
#os.system('color 3f')
print()
print(Fore.BLUE + Style.BRIGHT + "Welcome to my song database!".center(135) + Fore.WHITE + Style.NORMAL)

menuOption = ""
while menuOption != "quit":
    print(Fore.BLUE + Style.BRIGHT + "Enter command. Type 'help' for help:" + Fore.WHITE + Style.NORMAL)
    menuOption = input()
    match menuOption:
        case "create":
            StartMenuHelpers.createUser(redisClient, mongoDatabase)
        case "login":
            user = StartMenuHelpers.loginUser(redisClient, mongoDatabase)
            if user != None:
                LoginMenuMain.loginMain(user, redisClient, mongoDatabase)
            else:
                print(Fore.BLUE + Style.BRIGHT + "Invalid login, try again!" + Fore.WHITE + Style.NORMAL)
        case "quit":
            print(Fore.BLUE + Style.BRIGHT + "Come again soon! :)" + Fore.WHITE + Style.NORMAL)
        case "karaoke":
            SharedMenuHelpers.playSong()
        case "help":
            StartMenuHelpers.displayHelp()
        case "_":
            print(Fore.BLUE + Style.BRIGHT + "Invalid command, type 'help' for help"  + Fore.WHITE + Style.NORMAL)




