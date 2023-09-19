import random
import time
import signal
import sys
import os

def signal_handler(sig, frame):
    sys.exit(0)

def display_word(word="", guessed=[]):
    print(" ".join([letter if letter in guessed else "_" for letter in word]), end="\n\n")
    return 0

def display_hanged(word="", wrong=0, difficulty=12):
    stages1 = [" __________          ",
                " |/                  ",
                " |                   ",
                " |                   ",
                " |                   ",
                " |                   ",
                "/|\                  "
                ]
    stages2 = [ " __________          ",
                " |/        |         ",
                " |         |         ",
                " |       (x.x)       ",
                " |        /|\        ",
                " |        / \        ",
                "/|\                  "
                ]
    # print("\n".join(list(map(str,stages1[-12-difficulty::]))), end="\n\n")
    if wrong <= 6 and wrong > 0 and wrong <= difficulty:
        print("\n".join(list(map(str,stages1[-wrong::]))), end="\n\n")
    elif wrong > 6:
        print("\n".join(list(map(str,stages2[0:wrong-(difficulty//2)]))))
        print("\n".join(list(map(str,stages1[-((difficulty//2)-wrong):]))), end="\n\n")

    return 0

def check_win(word="", guessed=[]):
    found = []
    sstring = ""
    found += [letter if letter in guessed else "_" for letter in word]
    sstring = "".join(found)
    if sstring.upper() == word.upper():
        return True
    else: return False

def hangman(word, difficulty=12):
    wrong = 0
    guessed = []
    while 1:
        display_word(word, guessed)
        display_hanged(word, wrong, difficulty)
        guess = input("guess a letter or the word: ").upper()
        # os.system('clear')
        if len(guess) > 1:
            if guess == word:
                guessed = list(word)
            else:
                print("Wrong guess!" + "\n" + guess + " is not the word.")
                wrong += 1
        elif len(guess) == 1 and guess in word and guess not in guessed:
            guessed.append(guess)
        else:
            print("Not " + guess + "!")
            wrong += 1
        if wrong >= difficulty:
            display_word(word, guessed)
            display_hanged(word, wrong, difficulty)
            return 1
        elif check_win(word, guessed) == True:
            print("BRAVOO")
            display_word(word, guessed)
            return 0

def main(argv):
    signal.signal(signal.SIGINT, signal_handler)
    with open('./wordlist.txt') as text:
        wordlist = text.read().splitlines()
    word = ""
    while word == "":
        word = random.choice(wordlist)
    start_time = time.time()
    res = hangman(word.upper(), int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 12)
    if res == 0:
        print("res = " + str(res))
        print("You win! The word was: " + word.title())
        print("Your time: " + str(time.time() - start_time) + " seconds.")
    else:
        print("You lose! The word was: " + word.title())
    return 0

main(sys.argv)