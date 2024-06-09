
import StartMenuHelpers

#from urllib2 import Request, urlopen

print("Welcome to my song database!")

menuOption = ""
while menuOption != "quit":
    print("Enter command. Type 'help' for help:")
    menuOption = input()
    match menuOption:
        case "create":
            StartMenuHelpers.createUser()
        case "login":
            loginResult = StartMenuHelpers.loginUser()
            if loginResult:
                loginMain()
        case "quit":
            print("Come again soon! :)")
        case "karaoke":
            StartMenuHelpers.playSong()
        case "help":
            StartMenuHelpers.displayHelp()
        case "_":
            print("Invalid command, type 'help' for help")


    def loginMain():
        print("another test")


