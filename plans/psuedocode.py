#Note: some parts of the plan changed in practice

#import dictionary
#import other variables from config


#import random

#roundNum, vowel list, wheelList, wordList and empty variables

#changed players dicitonary into 3 list. 
#functions:

#read in dictionary

#read wheelPieces

#prompt player names (test with defaults)

#gamesetup--call the 3 above functions

#getWord -- 1.choose a random word. To begin with, start with one word
#           2. Make list of word and underscore-only list of word

#RoundSetup--1.confirm each player rounds are still 0
#            2. Randomize player order (do not change player number in player dict)
#            3. call get word

#spinwheel 1. randomly choose a wheel value
           # . if bankrupt, end turn
           #3. if lose turn piece, end turn
           #4. store amount from wheel in a variable spinResult.
           #5. call guessletter(letter, player#)
           #6. if goodGuess = true, add pieceAmount to roundTotal and gameTotal
           #7. else, end turn

#guessLetter(letter, player#)

        # check if in alreadyGuessedLetters
            # if yes, goodGuess = false

            # if no, check if in chosenWord List
                # if in chosenWordList, 
                    # replace blankWordList
                    # count occurences of letter
                    # return goodGuess = true 
                # if not, 
                    # goodGuess = false
            #return goodGuess


#buyVowel(player#)
        # check player roundTotal
            #  if too low, 
                # goodGuess = false 
            #else
                # substract vowelCost from roundTotal
                #guessLetter()
            #return goodGuess

#guessWord(player#)
    #prompt word input 
    # if promptWord = targetWord
        #fill in blankWordList
    #else
        #print('incorrect")
    #return false

#wofTurn(player#)
    #prompt player to choose action
    
    #check for word completion after each turn
    

#wofRound()
        #call wofTurn

#wofFinalRound()

    #detect highest score player
    #getWord()
    #guessLetter(R S T L N E)
    #print blankWord
    #guessLetter(3 consonants, 1 vowel)
    #print blankWord
    #guessWord()
    #5 second timere
    #if guessedWord = targetWord
        #finalPrize + gameTotal
    #else
        #end game

#main