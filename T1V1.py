from random import randint
import math

Inputs = {
    "Play": ["p", "play", "restart", "r", "new game", "n"],
    "Set range": ["set", "new range", "change range", "switch range"],
    "End game": ["end", "stop", "break", "end game", "stop game", "break game", "exit"]
    }
default = [0, 100]

def play():
    option = ""
    while option != "end game":
        option = input(f'Choose to play the game, current settings:\n range: {default}\n: ').lower()
        match switch(option):
            case "play":
                startgame()
            case "set range":
                setrange()
            case "end game":
                option = "end game"
            case n_:
                print("Try again")

def checkscore():
    print("check score")
    pass

def resetscore():
    print("reset score")
    pass

def startgame():
    targetnumber = generatenumber(default[0],default[1])
    gamescore = 0
    loop, gamescore = iterategamestate(gamescore, targetnumber)
    while loop == True:
        loop, gamescore = iterategamestate(gamescore, targetnumber)


def switch(inputs):
    if inputs in Inputs["Play"]:
        return "play"
    elif inputs in Inputs["Set range"]:
        return "set range"
    elif inputs in Inputs["End game"]:
        return "end game"
    else:
        return "Try again"
    
def iterategamestate(gamescore, targetnumber):
    if gamescore == 10:
        print("Too many guesses, try again?")
        return False, gamescore
    loop = True
    guess = getplayerinput()
    if isinstance(guess, int):
        solved = HigherLower(guess, targetnumber, gamescore)
        gamescore += 1
    elif guess in Inputs["End game"]:
        loop = False
    else:
        print("Number?")
    return loop, gamescore
    
    
def getplayerinput():
    inputs = input("Input a number: ")
    try:
        inputs = int(inputs)
    except ValueError:
        print('Number?')
        pass
    return inputs

def setrange():
    minima = int(input("Minimum: "))
    maxima = int(input("Maxima: "))
    default = [minima, maxima]

def generatenumber(minima, maxima):
    return randint(minima,maxima)

def guessnumber():
    currentnumber = int(input("Guess :"))
    return currentnumber

def HigherLower(current, target, gamescore):
    if current < target:
        print("Too Low")
        return False
    elif current > target:
        print("Too High")
        return False
    else:
        print("You Win the correct number is " + str(target))
        print("Your score was " + str(gamescore))
        return True

def Computerscore():
    maxrange = default[1] - default[0]
    optomised_plays = math.log2(maxrange)
    return optomised_plays

if __name__ == "__main__":
    play()
