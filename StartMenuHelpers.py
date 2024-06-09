from colorama import Fore, Style
import bcrypt

def displayHelp():
    print(Fore.BLUE + Style.BRIGHT)
    print("create - creates a new user account")
    print("login - used to login to your account")
    print("quit - exit program")
    print("karaoke - used to play a song without logging in")
    print("help - display commands")
    print(Fore.WHITE + Style.NORMAL)

def createUser(redisClient, mongoDatabase):
    print(Fore.BLUE + Style.BRIGHT + "Enter your username:" + Fore.WHITE + Style.NORMAL)
    username = input()
    #TO DO:: check to see if the username is in your database somehow
    print(Fore.BLUE + Style.BRIGHT + "Enter password: " + Fore.WHITE + Style.NORMAL)
    passOne = input()
    print(Fore.BLUE + Style.BRIGHT + "Confirm password:" + Fore.WHITE + Style.NORMAL)
    passTwo = input()
    if passOne != passTwo:
        print(Fore.BLUE + Style.BRIGHT + "oops, try again!" + Fore.WHITE + Style.NORMAL)
        return
    
    #hash password
    passOneBytes = str.encode(passOne)
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(passOneBytes, salt)
    
    #check redis to see if not already taken
    # retrievedPass = redisClient.get(username)
    # if retrievedPass != None:
    #     print("username already taken, sorry")
       
    #check mongo to see if not already taken
    #searchUsername = mongoDatabase.Users.find({"username":username})
    if mongoDatabase.Users.count_documents({"username":username}) == 0:
        mongoDatabase.Users.insert_one({"username": username, "password": hashedPassword})
    else:
        print(Fore.BLUE + Style.BRIGHT + "Username already taken, sorry"  + Fore.WHITE + Style.NORMAL)
        return

    print(Fore.BLUE + Style.BRIGHT + "User created!" + Fore.WHITE + Style.NORMAL)

def loginUser(redisClient, mongoDatabase):
    print(Fore.BLUE + Style.BRIGHT + "Enter your username:" + Fore.WHITE + Style.NORMAL)
    username = input()
    print(Fore.BLUE + Style.BRIGHT  + "Enter password:" + Fore.WHITE + Style.NORMAL)
    password = input()
    passwordBytes = str.encode(password)
    #check redis to see if user in cache
    #retrievedPass = redisClient.get(username)
    # if retrievedPass != None:
    #     if retrievedPass == password:
    #         print("Success! Logging in")
    #         return username
    #     else:
    #         return None
    # else: #try looking for user in mongo db
    #searchUsers = mongoDatabase.Users.find({"username":username, "password":password})
    if mongoDatabase.Users.count_documents({"username":username}) == 1:
        hashedDatabasePassword = mongoDatabase.Users.find({"username":username}, {"_id": 0, "password": 1})
        hashedDatabasePassword = list(hashedDatabasePassword)
        if (bcrypt.checkpw(passwordBytes, hashedDatabasePassword[0]["password"])):
            return username
        else:
            print(Fore.BLUE + Style.BRIGHT + "Password doesn't match"  + Fore.WHITE + Style.NORMAL)
    else:
        print(Fore.BLUE + Style.BRIGHT + "Username not found, try again"  + Fore.WHITE + Style.NORMAL)
