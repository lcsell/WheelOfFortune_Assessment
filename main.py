from config import dictionaryloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import finalprize

#for random choices and the final round timer respectively
import random
import time

#global variables that will be refrenced throughout
players = []
playerRoundTotal = [0, 0, 0]
playerGameTotal = [0, 0, 0]
roundNum = 0
wordList = []
wheelList = []
roundWord = ""
roundWordList =[]
blankWord = ""
vowels = {"a", "e", "i", "o", "u"}
finalLetters = {"r","s","t","l","n","e"}
guessComplete = False
overallLetterCount = 0
alreadyGuessedLetters = []

#function to read in list of words
def readDictionaryFile():
    global wordList
    d = open(dictionaryloc, 'r')
    wordList = d.read().splitlines()

#function to read in Wheel of Fortune pieces 
def readWheelPieces():
    global wheelList
    w = open(wheeltextloc, 'r')
    wheelList = w.read().splitlines()

#function to get three player names
def playerInfo():
    global players

    print("We need three players. Enter their names.")
    p1 = str(input("Enter name 1: "))
    players.append(p1) 
    p2 = str(input("Enter name 2: ")) 
    players.append(p2)
    p3 = str(input("Enter name 3: ")) 
    players.append(p3) 

    print(f"Our players today are {p1}, {p2}, and {p3}.")

#function to set up the game initially
def gameSetup():
    global wordList
    readDictionaryFile()
    readWheelPieces()
    print("Welcome to Wheel of Fortune!")
    print("===========================")

    playerInfo()

#function to find a word for each round and its blank version
def getWord():
    global wordList
    global roundWord
    global roundWordList
    global blankWord

    roundWord = random.choice(wordList)
    roundWordList = list(roundWord)
    blankWord = "_" * len(roundWord) 
    
    print(f"The round's word is {blankWord}" )
    return roundWord, blankWord

#function to set up non-final rounds
def wofRoundSetup():
    global players
    global roundWord
    global roundWordList
    global blankWord
    global alreadyGuessedLetters
    global overallLetterCount

    alreadyGuessedLetters = []
    #reset roundTotalValues
    for i in range(len(playerRoundTotal)):
        if playerRoundTotal[i] != 0:
            playerRoundTotal[i] = 0
    
    #make sure overallLetterCount is refreshed to 0
    overallLetterCount = 0

    #select random player by name
    initName = random.choice(players)

    #associate random name with their player number
    initPlayer = (players.index(f'{initName}')) + 1

    print("=================")
    print(f"Player #{initPlayer} {initName} is going first!")
    print("=================")
    getWord()

    #return randomly selected first player
    return initPlayer

def spinWheel(playerNum):
    global wheelList
    global players
    global playerRoundTotal
    global vowels

    #find player index for tracking
    playerIndex = playerNum - 1

    #spin the wheel
    spinResult = random.choice(wheelList)

    #manage spin results
    if spinResult == "Bankrupt":
        playerRoundTotal[playerIndex] = 0
        print("Bankrupt!")
        stillinTurn = False

    elif spinResult == "LoseATurn":
        print("You landed on Lose a Turn")
        stillinTurn = False

    else:
        print(f"The wheel landed on ${spinResult}.")
        spinResult = int(spinResult)

        spinGuess = str(input("Please guess a consonant: "))

        #preventing free vowel guesses
        if spinGuess in vowels:
            print("You must buy a vowel")
            stillinTurn = False
        else:
            x, y = guessLetter(spinGuess, playerNum)

            playerRoundTotal[playerIndex] = playerRoundTotal[playerIndex] + (spinResult*x)

            print(f"{players[playerIndex]} has ${playerRoundTotal[playerIndex]} total!")
            stillinTurn = y
     
    return stillinTurn

#function for guessing letters
def guessLetter(letter, playerNum):
    global players
    global vowels
    global blankWord
    global roundWord
    global roundWordList
    global guessComplete
    global overallLetterCount
    global alreadyGuessedLetters

    letterCount = 0
    goodGuess = True
    
    #checking if letter has been guessed already
    if letter in alreadyGuessedLetters:
        print("That letter has already been guessed")
        goodGuess = False
    else:
        #checking if letter is in the target word
        if letter in roundWordList:
            alreadyGuessedLetters.append(letter)
            #displaying the target word with underscores for unguessed letters
            pos = [i for i in range(len(roundWord)) if roundWord.startswith(letter,i)]
            for i in pos:
                blankWord = blankWord[:i] + letter + blankWord[i+len(letter):]
                letterCount += 1
                overallLetterCount += 1
                print(blankWord)
                print(f"{letter} occured {letterCount} times")
                    
                #checking for word completion
                if overallLetterCount == len(roundWord):
                    guessComplete = True
                    goodGuess = False
                else:
                    goodGuess = True

         #if a letter is not in the target word       
        else:
            print("Not in word.")
            goodGuess = False

    return letterCount, goodGuess

#function for buying vowels in Wheel of Fortune
def buyVowel(playerNum):
    global players
    global playerRoundTotal
    global vowels
    global overallLetterCount
    global roundWord
    global guessComplete 

    #find player index for tracking
    playerIndex = playerNum - 1
    
    #check if player has enough money for a vowel purchase
    if playerRoundTotal[playerIndex] < vowelcost:
        print(f"{players[playerIndex]} has insufficient funds")
        goodGuess = False
    else:
        playerRoundTotal[playerIndex] = playerRoundTotal[playerIndex] - vowelcost
        vowelGuess = str(input("Guess a vowel: "))
        #ensuring guess is a vowel. The variable y was needed to keep goodGuess accurate.
        if vowelGuess in vowels:
            x, y = guessLetter(vowelGuess, playerNum)
            print(f"{players[playerIndex]} has ${playerRoundTotal[playerIndex]} in the bank")
            goodGuess = y
        else:
            print("That is not a vowel")
            print(f"{players[playerIndex]} has ${playerRoundTotal[playerIndex]} in the bank")
            goodGuess = False
    
    return goodGuess

#function for guessing the target word in its entirety
def guessWord(playerNum):
    global players 
    global roundWord
    global blankWord
    global guessComplete
    global playerRoundTotal

    playerIndex = playerNum - 1

    fullGuess = str(input("Guess the entire word: "))

    #check if guess is correct

    if fullGuess == roundWord:
        guessComplete = True
        print(f"{players[playerIndex]} guessed correctly!")
        playerRoundTotal[playerIndex] = playerRoundTotal[playerIndex] + 1000
        print(f"{players[playerIndex]} now has ${playerRoundTotal[playerIndex]}!")

    else:
        print("That is not the word")
        
    #indicate turn will finish
    return False


#function to conduct player turns
def wofTurn(playerNum):
    global roundWord
    global blankWord
    global players
    global playerRoundTotal
    global guessComplete

    playerIndex = playerNum - 1
    stillInTurn = True
    
    #loop to manage player options
    while guessComplete == False:
        print(f"It's {players[playerIndex]}'s turn!")
        while stillInTurn == True:
            choice = str(input("Please enter s to spin, b to buy a vowel, or g to guess the word: "))
            if(choice.strip().upper() == "S"):
                stillInTurn = spinWheel(playerNum)
            elif(choice.strip().upper() == "B"):
                stillInTurn = buyVowel(playerNum)
            elif(choice.upper() == "G"):
                stillInTurn = guessWord(playerNum)
            else:
                print("Not a correct option")
        else:
            print(f"End of {players[playerIndex]}'s turn!")
            print("====================")
            break
    
    return guessComplete

#function to manage non-final rounds
def wofRound():
    global players
    global playerRoundTotal
    global roundWord
    global blankWord
    global guessComplete
    global roundNum
    global overallLetterCount
    global playerGameTotal

    guessComplete = False

    #choose first player
    initPlayer = wofRoundSetup()

    #establish player order
    initPlayerIndex = initPlayer - 1
    
    if initPlayerIndex <= 1:
        secondPlayer = initPlayer + 1
    else:
        secondPlayer = 1

    secondPlayerIndex = secondPlayer - 1

    if secondPlayerIndex <= 1:
        thirdPlayer = secondPlayer + 1
    else:
        thirdPlayer = 1

    #announce beginning of round
    print(f"Round {roundNum + 1} has begun!")
    print("====================")

    #play turns
    while not guessComplete:  
        wofTurn(initPlayer)
        wofTurn(secondPlayer)
        wofTurn(thirdPlayer)

    #announce end of round
    print('End of round!')

    #display round totals for each player
    print(f'''
    In this round, {players[0]} earned ${playerRoundTotal[0]}, 
    {players[1]} earned ${playerRoundTotal[1]}, 
    and {players[2]} earned ${playerRoundTotal[2]} ''')
    
    #record number of rounds
    roundNum += 1

    #adding roundTotal to gameTotal
    playerGameTotal[0] = playerRoundTotal[0] + playerGameTotal[0]
    playerGameTotal[1] = playerRoundTotal[1] + playerGameTotal[1]
    playerGameTotal[2] = playerRoundTotal[2] + playerGameTotal[2]

    #print out gameTotal
    print(f'''
    So far this game, {players[0]} has earned ${playerGameTotal[0]}, 
    {players[1]} has earned ${playerGameTotal[1]}, 
    and {players[2]} has earned ${playerGameTotal[2]}''')

    print("====================")

#function to conduct final round
def wofFinalRound():
    global roundWord
    global roundWordList
    global blankWord
    global players
    global playerGameTotal
    global alreadyGuessedLetters
    
    print("It's the final round!")
    print("====================")
    #set up round and select top scoring player to compete in final round
    alreadyGuessedLetters = []

    biggestBank = max(playerGameTotal)

    finalPlayerIndex = playerGameTotal.index(biggestBank)

    finalPlayer = players[finalPlayerIndex]

    #text introduction for user. Empty strings added for user readability
    print(f"Our final player is {finalPlayer}!")
    print("")
    print(f"{finalPlayer} has five seconds to guess the final word for a grand prize of ${finalprize}!")
    print("")
    print(f"The letters {finalLetters} will be provided freely")
    print("")
    print(f"After that, {finalPlayer} can choose 3 consonants and 1 vowel afterward.")
    print("")
    print(f"Finally, {finalPlayer} will have 5 seconds to guess the word.")

    #get a new word
    getWord()

    #display final word with freely given letters filled in
    print(f"Let's check for {finalLetters}")
    guessLetter("r", 1)
    guessLetter("s", 1)
    guessLetter("t", 1)
    guessLetter("l", 1)
    guessLetter("n", 1)
    guessLetter("e", 1)

    #user inputs their 4 letters. letters are checked for appropriateness
    consonant1 = str(input("First consonant: "))
    if consonant1 in finalLetters:
        print("That was already guessed")
    elif consonant1 in vowels:
        print("That's not a consonant!")
    else:
        guessLetter(consonant1, 1)

    consonant2 = str(input("Second consonant: "))
    if consonant2 in finalLetters:
        print("That was already guessed")
    elif consonant2 in vowels:
        print("That's not a consonant!")
    else:
        guessLetter(consonant2, 1)

    consonant3 = str(input("Third consonant: "))  
    if consonant3 in finalLetters:
        print("That was already guessed")
    elif consonant3 in vowels:
        print("That's not a consonant!")
    else:
        guessLetter(consonant3, 1)

    lastVowel = str(input("Vowel: "))
    if lastVowel in finalLetters:
        print("That was already guessed")
    elif lastVowel not in vowels:
        print("That's not a vowel!")
    else:
        guessLetter(lastVowel, 1)

    
    #Final imput for solution and five second timer
    time1 = time.time()
    finalGuess = str(input('Guess the full word: '))
    time2= time.time()
    timeElapsed = time2 - time1
    if timeElapsed > 5:
        print(f"{finalPlayer} ran out of time!")
        print(f"The word was {roundWord}")
        print("The game is over")
    else:
        if finalGuess == roundWord:
            print('Congrats!!')
            playerGameTotal[finalPlayerIndex] += finalprize
            print(f"{players[finalPlayerIndex]} has won the generous final prize amount of ${finalprize} for a grand total of ${playerGameTotal[finalPlayerIndex]}")
        else:
            print("Horrible! The game is over.")
            print(f"The word was {roundWord}")

#function to run game as a whole
def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

#code to run one game
if __name__ == "__main__":
    main()
    

