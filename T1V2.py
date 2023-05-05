from random import randint
import math

Inputs = {
    "Play": ["p", "play", "restart", "r", "new game", "n"],
    "Set range": ["set", "new range", "change range", "switch range", "range"],
    "Check score": ["score", "high score", "scores", "history", "stats"],
    "Reset score": ["reset score", "reset scores", "reset high score", "reset history", "reset stats", "reset"],
    "End game": ["end", "stop", "break", "end game", "stop game", "break game", "", "done", "exit"],
    "Easy mode": ["e", "easy", "not hard", "simple", "newbie", "training"],
    "Hard mode": ["h", "hard", "not easy", "complex", "challenge"],
    "Help": ["help", "/help", "guide"],
    "Play computer": ["comp", "p comp", "play c", "play comp"]
    }
default = [0, 100]

playerpath = []

playerscore = []

player_range = [0, 100]

computer_range = [0,100]


def play():
    option = ""
    global easymode
    easymode = False
    while option != "end game":
        player_range[0] = default[0]
        player_range[1] = default[1]
        print(f"\nEasy mode: {easymode}\n")
        option = input(f'Choose to play the game, current settings:\n range: {default}\n: ').lower()
        match switch(option):
            case "play":
                startgame()
            case "set range":
                setrange()
            case "check score":
                checkscore()
            case "reset score":
                resetscore()
            case "end game":
                option = "end game"
            case "easy mode":
                easymode = True
            case "hard mode":
                easymode = False
            case "help":
                showhelp()
            case "play comp":
                Playcomp()
            case n_:
                print("Try again")

def checkscore():
    print(f"Your score from the past games are: {', '.join(playerscore)}\n")
    pass

def resetscore():
    playerscore.clear()
    print("Scores are reset")
    pass

def showhelp():
    print("Commands:")
    for key, item in Inputs.items():
        print(f"{key}: {', '.join(item)}\n")

def startgame():
    targetnumber = generatenumber()
    gamescore = 0
    loop, gamescore = iterategamestate(gamescore, targetnumber)
    while loop == True:
        loop, gamescore = iterategamestate(gamescore, targetnumber)

def resetcomputer():
    computer_range[0] = default[0]
    computer_range[1] = default[1]

def switch(inputs):
    if inputs in Inputs["Play"]:
        return "play"
    elif inputs in Inputs["Set range"]:
        return "set range"
    elif inputs in Inputs["Check score"]:
        return "check score"
    elif inputs in Inputs["Reset score"]:
        return "reset score"
    elif inputs in Inputs["End game"]:
        return "end game"
    elif inputs in Inputs["Easy mode"]:
        return "easy mode"
    elif inputs in Inputs["Hard mode"]:
        return "hard mode"
    elif inputs in Inputs["Help"]:
        return "help"
    elif inputs in Inputs["Play computer"]:
        return "play comp"
    else:
        return "Try again"

def Playcomp():
    resetcomputer()
    targetnumber = generatenumber()
    compsolved = False
    playersolved = False
    playerscore = 0
    compguess = computerguess()
    playerguess = getplayerinput()
    if playerguess in Inputs["End game"]:
        playersolved = True
    while compsolved != True and playersolved != True:
        compsolved, compHigher = HigherLower(compguess, targetnumber, 0, Player=False)
        playersolved, playerHigher = HigherLower(playerguess, targetnumber, playerscore)
        playerscore += 1
        if playersolved and compsolved == False:
            print("You beat the computer!")
            break
        elif playersolved and compsolved:
            print("It's a tie")
            break
        elif compsolved:
            print(f"The computer won, the number was {compguess}")
            break
            

        
        #Give the player the computer's guess
        if compHigher:
            print(f"The computer guessed {compguess} and it is too High")
        else:
            print(f"The computer guessed {compguess} and it is too Low")

        #Update the computer's range

        Cguess = [compguess, compHigher]
        Pguess = [playerguess, playerHigher]
        updatecomputerrange(Cguess, Pguess)


        compguess = computerguess()
        playerguess = getplayerinput()
        if playerguess in Inputs["End game"]:
            playersolved = True
        
def updatecomputerrange(computerguess, playerguess):

    if computerguess[0] < computer_range[1] and computerguess[1]:
        computer_range[1] = computerguess[0]
    elif computerguess[0] > computer_range[0] and computerguess[1] == False:
        computer_range[0] = computerguess[0]


    #Evaluating the player's guesses

    if playerguess[0] < computer_range[1] and playerguess[1]:
        computer_range[1] = playerguess[0]
    elif playerguess[0] > computer_range[0] and playerguess[1] == False:
        computer_range[0] = playerguess[0]



def computerguess():
    nextguess = int(computer_range[0]/2 + computer_range[1]/2)
    return nextguess
    

def iterategamestate(gamescore, targetnumber):
    if gamescore == 10:
        print("Too many guesses, try again?")
        return False, gamescore
    loop = True
    guess = getplayerinput()
    if isinstance(guess, int):
        solved, playerHigher = HigherLower(guess, targetnumber, gamescore)
        gamescore += 1
        if solved:
            loop = False
    elif guess in Inputs["End game"]:
        loop = False
    else:
        print("Number?")
    return loop, gamescore
    
    
def getplayerinput():
    inputs = input("Input a number: ").lower()
    try:
        inputs = int(inputs)
    except ValueError:
        pass
    return inputs

def setrange():
    minima = int(input("Minimum: "))
    maxima = int(input("Maxima: "))
    default[0] = minima
    default[1] = maxima

def generatenumber():
    return randint(default[0],default[1])

def guessnumber():
    currentnumber = int(input("Guess :"))
    return currentnumber

def HigherLower(current, target, gamescore, Player = True):
    playerpath.append(current)
    if current < target:
        if easymode and Player:
            print("Too Low\n")
            UpdatePlayerrange(False, current)
        elif Player:
            print("Too Low\n")
        return False, False
    elif current > target:
        if easymode and Player:
            print("Too High\n")
            UpdatePlayerrange(True, current)
        elif Player:
            print("Too High\n")
        return False, True
    elif Player:
        print("the correct number is " + str(target))
        print("Your score was " + str(gamescore))
        playerscore.append(str(gamescore))
        return True, None
    else:
        return True, None

def UpdatePlayerrange(Higher, current):
    #Higher checks if the guessed number is bigger or smaller
    if Higher and player_range[1] >= current:
        player_range[1] = current - 1
    elif Higher == False and player_range[0] <= current:
        player_range[0] = current + 1
    else:
        print("Your playing on easy mode and still getting it wrong!?!?!?\n")
    Prange = ""
    if player_range[1] - player_range[0] < 10:
        Prange = ", ".join([str(n) for n in range(player_range[0], player_range[1] + 1)])
    else:
        Prange = str(player_range[0]) + "".join("-" for i in range(player_range[0], player_range[1], 10)) + str(player_range[1])
    print(f"Player range: {Prange}\n")

def Computerscore():
    maxrange = default[1] - default[0]
    optomised_plays = math.log2(maxrange)
    return optomised_plays

if __name__ == "__main__":
    play()
