import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
# taking wordlist txt file to load in program
WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


def displayHand(hand):
    """
    display the hand in staright line
    """
    print('Current Hand:', end=' ')
    for key in hand:
        if hand[key] != 0:
            # print all on the same line
            for i in range(hand[key]):
                print(key, end=' ')
    # for next line
    print()
    return None


def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    length = len(word)
    sum = 0
    # calculating the sum
    for e in word:
        sum += SCRABBLE_LETTER_VALUES[e]
    sum *= length
    # adding bonus points if first guessed word is of length n
    if length == n:
        sum += 50
    return sum


def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    numVowels = n // 3
    # to give 1/3 characters of hand as vowels
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
    # remaining as consonants
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
    return hand


def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # new temporary dic for not changing original hand
    updated_hand = {}
    # assigning indirectly to avoid aliasing problems
    for element in hand:
        updated_hand[element] = hand[element]
    # initializing new array
    for element in word:
        updated_hand[element] -= 1
    return updated_hand


def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    try:
        # empty word is invalid
        if len(word) == 0:
            return False
        for element in word:
            num = word.count(element)
            # if some character count in word is more than allowded by hand
            if hand[element] < num:
                return False
        # if word is not a correct word from wordList
        if word not in wordList:
            return False
        return True
    # if any wrong type input is presented. invalid
    except:
        return False


def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for elements in hand:
        length += hand[elements]
    print(length)
    return length


def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    total = 0
    while True:
        try:
            # if hand is empty or all letters are used up
            if calculateHandlen(hand) <= 0:
                print("Run out of letters. Total score: %i points." % total)
                break
            print('Current Hand:', end=' ')
            displayHand(hand)
            # user provided word
            word = input("Enter word, or a '.' to indicate that you are finished: ")
            if word == '.':
                print("Goodbye! Total score: %i points." % total)
                return 0
            # condition to check for valid string input
            if word.isalpha() != True:
                raise Exception
        except:
            # non alphabetic type error handled
            print("Invalid word, please try again.")
            # to return to start of the loop
            continue
        else:
            # if word is invalid
            if not isValidWord(word, hand, wordList):
                print("Invalid word, please try again.")
            else:
                # word is valid
                # x = temporary score handler
                x = getWordScore(word, n)
                total += x
                print('"%s" earned %i points. Total: %i points' % (word, x, total))
                # updating hand by removing user valid words
                hand = updateHand(hand, word)
    return 0


def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    # start of game
    first_game = True
    while True:
        user = input("Enter n to deal a new hand, r to replay the last hand, or e to end game:")
        # ending game
        if user == 'e':
            break
        elif user == 'r' and first_game == True:
            print("You have not played a hand yet. Please play a new hand first!")
        elif user == 'r':
            playHand(hand, wordList, HAND_SIZE)
        elif user == 'n':
            first_game = False
            # selecting random size of hand
            HAND_SIZE = random.randrange(5, 10)
            # generating hand
            hand = dealHand(HAND_SIZE)
            # play the game
            playHand(hand, wordList, HAND_SIZE)
        else:
            print("Invalid command.")
    return 0


wordList = loadWords()

# Below command is optional. If you want to play just with user then uncomment
# it and play the game. else use usercomputer.py file to run the whole game

# playGame(wordList)