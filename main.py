"""
Filename: main.py
Project: WordleBot
Name: Gautam Mitra
Last Updated: 02/5/2022
Purpose: Create an interactive solver for popular online word game Wordle
"""
import sys
import string

def main():


    # Read in list of valid words in Wordle and create dictionary
    word_dict = {}
    with open("./ValidWords.txt", "r") as reader:
        word_list = reader.read().split(",")
        for word in word_list:
            word_dict[word] = [word[0], word[1], word[2], word[3], word[4]]


    # Create set of allowed characters in result
    allowed = set(["b", "y", "g", " "]) #black, yellow, green
    guess_count = 1
    corr_letter_count = 0
    while guess_count < 6 and corr_letter_count < 5:
        while True: # Take in user guesses
            user_guess = input(f"Input guess #{guess_count}: ")
            if len(user_guess) == 5:
                guess_count += 1
                break

        while True: # Take in the wordle feedback to the user's guess
            result = input("Input result of guess (e.g. b b g g y)")
            if len(result) == 9 and set(result) <= allowed:
                corr_letter_count = result.count("g")
                break          

        print(user_guess, result)

if __name__ == "__main__":
    main()