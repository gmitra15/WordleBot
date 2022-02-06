"""
Filename: main.py
Project: WordleBot
Name: Gautam Mitra
Last Updated: 02/5/2022
Purpose: Create an interactive solver for popular online word game Wordle
"""
import sys
import re

def main():


    # Read in list of valid words in Wordle and create dictionary
    rem_words = {}
    with open("./ValidWords.txt", "r") as reader:
        word_list = reader.read().split(",")
        for word in word_list:
            rem_words[word] = [word[0], word[1], word[2], word[3], word[4]]


    # Create set of allowed characters in result
    allowed = set(["b", "y", "g"]) #black, yellow, green
    guess_count = 1
    green_letter_count = 0
    green_letters = []

    while guess_count < 6 and green_letter_count < 5:
        while True: # Take in user guesses
            user_guess = input(f"Input guess #{guess_count}: ")
            if len(user_guess) == 5:
                guess_count += 1
                break

        while True: # Take in the wordle feedback to the user's guess
            result = input("Input result of guess (e.g. bbggy)")
            if len(result) == 5 and set(result) <= allowed:
                green_letter_count = result.count("g")
                green_letters_idx = [letter.start() for letter in re.finditer('g', result)]
                break          

        # End the program if everything is correct
        if result == "ggggg":
            print("Correct word guessed!")
            sys.exit()
        else: # if the user didn't get the word correct, remove it from the list of plausible answers
            del rem_words[user_guess] 
 
        # Strip out all words from the list of remaining words that don't have a green letter in the right spot
        for green_letter in green_letters_idx:
            for word, letters in dict(rem_words).items():
                if word[green_letter] != user_guess[green_letter]:
                    del rem_words[word]
                

        print(f"Your next guess should be one of the following: {', '.join([key for key in rem_words.keys()])}")


if __name__ == "__main__":
    main()