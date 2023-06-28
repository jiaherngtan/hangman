import random
from flask import Flask, render_template, request, redirect, jsonify
import os

app = Flask(__name__)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def chooseWord(wordlist):
    return random.choice(wordlist)


wordlist = loadWords()


def isWordGuessed(secretWord, lettersGuessed):
    for l in secretWord:
        if l not in lettersGuessed:
            return False
    return True


def getGuessedWord(secretWord, lettersGuessed):
    word = ""
    for i in range(0, len(secretWord)):
        if secretWord[i] in lettersGuessed:
            word += secretWord[i]
        else:
            word += "_"
        word += " "
    return word


def getAvailableLetters(lettersGuessed):
    letters = list("abcdefghijklmnopqrstuvwxyz")
    for l in lettersGuessed:
        if l in letters:
            letters.remove(l)
    return letters


secretWord = chooseWord(wordlist).lower()
length = len(secretWord)
lettersGuessed = []
status = True
guesses = 8
update = ""


@app.route("/restart")
def restart():
    global secretWord
    global length
    global lettersGuessed
    global status
    global guesses
    global update

    secretWord = chooseWord(wordlist).lower()
    length = len(secretWord)
    lettersGuessed = []
    status = True
    guesses = 8
    update = ""
    return redirect("/")


@app.route('/')
def index():
    global status
    global guesses
    global update
    if request.method == "GET":
        # display
        letters = getAvailableLetters(lettersGuessed)
        if guesses == 0:
            word = secretWord
        else:
            word = getGuessedWord(secretWord, lettersGuessed)
        return render_template("index.html",
                           status=status,
                           length=length,
                           guesses=guesses,
                           update=update,
                           word=word,
                           letters=letters)
    else:
        # display
        letters = getAvailableLetters(lettersGuessed)
        word = getGuessedWord(secretWord, lettersGuessed)
        letter = request.form.get("letter")
        lettersGuessed.append(letter)
        if isWordGuessed(secretWord, lettersGuessed):
            update = "Congratulations, you won!"
            status = False
        elif letter in secretWord:
            update = "Good guess!"
        else:
            guesses -= 1
            update = "Oops! That letter is not in my word."
            if guesses == 0:
                update = "Sorry, you ran out of guesses."
                status = False
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
