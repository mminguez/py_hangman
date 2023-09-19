import random
import time
import signal
import sys

def signal_handler(sig, frame):
    sys.exit(0)

def display_word(word="", guessed=[]):
    print(" ".join([letter if letter in guessed else "_" for letter in word]), end="\n\n")
    return 0

def display_hanged(word="", wrong=0):
    stages1 = ["",
                " __________          ",
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
                " |         O         ",
                " |        /|\        ",
                " |        / \        ",
                "/|\                  "
                ]
    if wrong <= 7 and wrong > 0:
        print("\n".join(list(map(str,stages1[-wrong::]))), end="\n\n")
    elif wrong > 7:
        print("\n".join(list(map(str,stages2[0:wrong-6]))))
        print("\n".join(list(map(str,stages1[-(6-wrong):]))), end="\n\n")

    return 0

def hangman(word):
    wrong = 0
    guessed = []
    while len(guessed) < len(word):
        display_word(word, guessed)
        display_hanged(word, wrong)
        guess = input("guess a letter or the word: ").upper()
        if len(guess) > 1:
            if guess == word:
                guessed = list(word)
            else:
                wrong += 1
        elif len(guess) == 1 and guess in word and guess not in guessed:
            guessed.append(guess)
        else:
            wrong += 1
        if wrong >= 12:
            display_hanged(word, wrong)
            return 1
        elif len(guessed) == len(word):
            display_word(word, guessed)
            return 0
    return 1

def main():
    signal.signal(signal.SIGINT, signal_handler)
    with open('./wordlist.txt') as line:
        wordlist = line.read().splitlines()
    word = ""
    while word == "":
        word = random.choice(wordlist)
    start_time = time.time()
    res = hangman(word.upper())
    if res == 0:
        print("You win! The word was: " + word.title())
        print("Your time: " + str(time.time() - start_time) + " seconds.")
    else:
        print("You lose! The word was: " + word.title())
    return 0

main()