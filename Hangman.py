#!/usr/bin/env python3

# Hangman_GUI main game file with application layout and game logic

# *** ADD FEATURE - High Score
# ** Make start button nicer
# * Check if is possible to add image or something while loading from API

from Wordlist import world_list
import PySimpleGUI as psg
import random
import string
import requests
import webbrowser

version = "beta"

# Dictionary with all images used in the game
hangman_img = {
    10: "img/Hangman_10.png",
    9: "img/Hangman_09.png",
    8: "img/Hangman_08.png",
    7: "img/Hangman_07.png",
    6: "img/Hangman_06.png",
    5: "img/Hangman_05.png",
    4: "img/Hangman_04.png",
    3: "img/Hangman_03.png",
    2: "img/Hangman_02.png",
    1: "img/Hangman_01.png",
    0: "img/Hangman_00.png",
    "splash": "img/splash.png",
    "close": "img/close.png"
}

# Customization
# Install "RobotoMono-Regular.ttf" (main folder) for best experience, but app will still work without it :)
font_used = ('Roboto Mono', 10)
# Change theme
psg.theme("black")


def secret_word_api():
    # Get secret word from API and choose only words <= 12 characters long
    url = "https://random-word-api.herokuapp.com/word"
    response = requests.get(url)
    text = response.json()
    word = text[0]
    if len(word) <= 12:
        return word
    else:
        return secret_word_api()


def word_api_or_random():
    # Error handling in case API didn't work for some reason
    try:
        word = secret_word_api().upper()
    # Error handling
    except (requests.ConnectionError, requests.HTTPError, requests.exceptions.JSONDecodeError):
        word = random.choice(world_list).upper()
    return word


def check_word_meaning_link(word):
    # Create link to check the meaning of the secret word
    url = f"https://www.google.com/search?q={word.lower()}+meaning"
    return url


def splash_screen():
    # Define the layout for the splash screen
    splash_layout = [
        [psg.Image(hangman_img["splash"])],
        [psg.Button("START", font=(font_used[0], 16),
                    border_width=0,
                    key="-START-",
                    button_color="white")],
        [psg.VPush()],
        [psg.Text(f"Version: {version}", font=(font_used[0], 9))],
        [psg.Text("Click to visit my GitHub",
                  font=font_used, text_color="light green",
                  enable_events=True, key="-LINK-")]
    ]
    # Create the splash screen window
    splash_window = psg.Window('Splash', splash_layout,
                               size=(300, 570),
                               element_justification="center",
                               finalize=True,
                               no_titlebar=True,
                               grab_anywhere=True,
                               keep_on_top=True)
    # Show the splash screen and wait for the start button to be pressed
    while True:
        event, values = splash_window.read()
        if event == "-START-":
            break
        elif event == "-LINK-":
            webbrowser.open("https://github.com/paichiwo")

    # Close the splash screen window
    splash_window.close()


def game_window(points):
    # Main Game Layout
    game_layout = [
        [psg.VPush()],
        [psg.Push(), psg.Image("img/close.png",  # Close button
                               pad=0, enable_events=True, key="-CLOSE-")],
        [psg.VPush()],
        [psg.Image((hangman_img[10]), key="-HANGMAN-")],
        [psg.Text("", key="-WORD-", font=(font_used[0], 25))],
        [psg.Text("USED LETTERS:", font=font_used)],
        [psg.Text("", key="-USED-LETTERS-", font=(font_used, 9))],
        [psg.Text("LIVES", font=font_used),
         psg.Text("", key="-LIVES-", font=(font_used[0], 16), text_color="green"),
         psg.Push(),
         psg.Text(str(points), key="-POINTS-", font=(font_used[0], 16), text_color="green"),
         psg.Text("POINTS", font=font_used)],
        [psg.Text("GUESS A LETTER:", font=font_used)],
        [psg.Input("", size=(10, 1),
                   enable_events=True,
                   key="-INPUT-")],
        [psg.Button('Submit', visible=False, bind_return_key=True)],
        [psg.Text("", key="-OUTPUT-Msg-", font=font_used, text_color="yellow")],
        [psg.VPush()]
    ]
    # Create main game window
    window = psg.Window("Hangman Game", game_layout,
                        size=(300, 570),
                        element_justification="center",
                        finalize=True,
                        no_titlebar=True,
                        grab_anywhere=True,
                        keep_on_top=True)
    return window


def hangman(points=0):
    # Game logic

    window = game_window(points)

    # list with alphabet
    alphabet = string.ascii_letters
    # secret word
    word = word_api_or_random()
    print(word)
    # create a Google search link for user to check the meaning of the secret word
    link = check_word_meaning_link(word)
    # word letters as list
    word_letters = list(word)
    # word blanks as list
    word_blanks = ["_"] * len(word)
    # number of lives
    lives = 10
    # letters already used
    guessed_letters = ""

    window["-WORD-"].update("".join(word_blanks), font=(font_used[0], 25))
    window["-USED-LETTERS-"].update(", ".join(guessed_letters))
    window["-HANGMAN-"].update(hangman_img[lives])
    window["-LIVES-"].update(str(lives))

    # Main Loop
    while lives > 0:

        event, values = window.read()
        if event in (psg.WIN_CLOSED, "-CLOSE-"):
            break

        # accepts only one character, must be from alphabet
        if len(values["-INPUT-"]) > 1 or values["-INPUT-"] not in alphabet:
            # delete last char from input
            window["-INPUT-"].update(values["-INPUT-"][:-1])
        # if enter is pressed
        elif event == 'Submit':
            user_input = window["-INPUT-"].get().upper()
            window['-INPUT-'].update("")

            # Check if user_input in guessed letters
            if user_input not in guessed_letters:
                guessed_letters += user_input
                window["-USED-LETTERS-"].update(", ".join(guessed_letters))

                # Check if user_input is in word_letters list
                if user_input in word_letters:
                    window["-OUTPUT-Msg-"].update("Good guess, letter found")

                    # find indexes of correctly guessed letter
                    for i, letter in enumerate(word_letters):
                        # and replace blanks with letters
                        if word_letters[i] == user_input:
                            word_blanks[i] = word[i]
                    # output updated word
                    window["-WORD-"].update("".join(word_blanks), font=(font_used[0], 25))

                    # win condition
                    if "".join(word_blanks) == "".join(word_letters):
                        points += 1
                        window["-POINTS-"].update(str(points))
                        choice = psg.popup_yes_no(f"YOU WON! \nFind the meaning of: {word} ?\n",
                                                  font=font_used, keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        window.close()
                        hangman(points)
                # lost condition
                else:
                    lives = lives - 1
                    window["-OUTPUT-Msg-"].update("Wrong, try again!")
                    window["-HANGMAN-"].update(hangman_img[lives])
                    window["-LIVES-"].update(lives)
                    window["-WORD-"].update("".join(word_blanks), font=(font_used[0], 25))
                    if lives == 0:
                        choice = psg.popup_yes_no(
                            f"YOU LOST! \nDo you want to find the meaning\nof the word: {word} ?\n",
                            font=font_used, keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        window.close()
                        hangman(points)

            # output if letter already been chosen
            else:
                window["-OUTPUT-Msg-"].update("Letter used already!")

    window.close()


if __name__ == '__main__':
    splash_screen()
    hangman()
