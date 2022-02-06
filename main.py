"""
Filename: main.py
Project: WordleBot
Name: Gautam Mitra
Last Updated: 02/5/2022
Purpose: Create an interactive solver for popular online word game Wordle
"""
import sys
import re
import random

def main():


    # Read in list of valid words in Wordle and create dictionary
    rem_words = {}
    with open("./test_wordl_bank.txt", "r") as reader:
        word_list = reader.read().split(",")
        for word in word_list:
            rem_words[word] = [word[0], word[1], word[2], word[3], word[4]]

    # Create set of allowed characters in result
    allowed = set(["r", "y", "g"]) #black, yellow, green
    guess_count = 1
    green_letter_count = 0

    while guess_count < 6 and green_letter_count < 5:
        while True: # Take in user guesses
            user_guess = input(f"Input guess #{guess_count}: ")
            if len(user_guess) == 5:
                guess_count += 1
                break

        while True: # Take in the wordle feedback to the user's guess
            result = input("Input result of guess (e.g. RRGGY == gRey gRey Green Green Yellow): ").lower()
            if len(result) == 5 and set(result) <= allowed: # if valid input, continue
                green_letter_count = result.count("g")
                green_letters_idx = [letter.start() for letter in re.finditer('g', result)]

                grey_letter_count = result.count("r")
                grey_letters_idx = [letter.start() for letter in re.finditer('r', result)]

                yellow_letter_count = result.count("y")
                yellow_letters_idx = [letter.start() for letter in re.finditer('y', result)]
                break          

        # End the program if everything is correct
        if result == "ggggg":
            print("Correct word guessed!")
            sys.exit()
        else: # if the user didn't get the word correct, remove it from the list of plausible answers
            if user_guess in rem_words:
                del rem_words[user_guess] 
 
        # STEP 1: Strip out all words from the list of remaining words that don't have a green letter in the right position
        # Determine correct letters
        green_letters = []
        for idx, letter in enumerate(user_guess):
            if idx in green_letters_idx:
                green_letters.append(letter)
        
        for green_letter in green_letters_idx:
            for word, letters in dict(rem_words).items():
                if word[green_letter] != user_guess[green_letter]:
                    del rem_words[word]

        # STEP 2: Strip out all words that don't contain a yellow letter at all
        yellow_letters = []
        for idx, letter in enumerate(user_guess):
            if idx in yellow_letters_idx:
                yellow_letters.append(letter)
        
        print(f"Yellow Letters: {yellow_letters}")
        for yellow_letter in yellow_letters:
            for word, letters in dict(rem_words).items():
                if yellow_letter not in word:
                    del rem_words[word]

        # STEP 2A: Strip out all words that contain a yellow letter in the inputted position (right letter, wrong spot)
        for yellow_letter in yellow_letters_idx:
            for word, letters in dict(rem_words).items():
                if word[yellow_letter] == user_guess[yellow_letter]:
                    del rem_words[word]


        # STEP 3: Strip out all words that contain grey letters (i.e. letters that aren't in the word in any position) #

        # Determine which letters should be removed
        grey_letters = []
        for idx, letter in enumerate(user_guess):
            if idx in grey_letters_idx and letter not in grey_letters:
                grey_letters.append(letter)
        
        # Remove the words with fully incorrect letters
        for grey_letter in grey_letters:
            for word, letters in dict(rem_words).items():
                if grey_letter in word and grey_letter not in green_letters:
                    del rem_words[word]

        print(f"Now removing the following letters: {grey_letters}. Fully correct letters: {green_letters}")
        # print(f"Your next guess should be one of the following: {', '.join([key for key in rem_words.keys()])}")
        rem_word_list = [key for key in rem_words.keys()]
        print(f"Make your next guess: {random.choice(rem_word_list)} ({1/len(rem_word_list)*100:0.02f}% chance of success)")


if __name__ == "__main__":
    main()