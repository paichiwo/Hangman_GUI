#!/usr/bin/env python3

# Hangman_GUI main game file with application layout and game logic

# Add feature - check meaning of secret words in wikipedia or english dictionary
# Make start button nicer
# Make hangman art nicer and change resolution from 200x300 to 280x280/280x300
# Check if is possible to add image or something while loading from API
# Experiment with new mono font
# Experiment with upper/lower case
# Fix bug - app closing. reason: image loading failure ???

from Wordlist import world_list
import PySimpleGUI as psg
import random
import requests

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

# Install "Young.ttf" (main folder) for best experience, but app will still work without it :)
font_used = "Young"
# Create window layout with PySimpleGUI
psg.theme("black")


def secret_word_api():
    url = "https://random-word-api.herokuapp.com/word"
    response = requests.get(url)
    text = response.json()
    word = text[0]
    if len(word) <= 11:
        return word
    else:
        return secret_word_api()


def word_api_or_random():
    try:
        word = secret_word_api().upper()
    # Error handling
    except requests.ConnectionError:
        word = random.choice(world_list).upper()
    except requests.HTTPError:
        word = random.choice(world_list).upper()
    except requests.exceptions.JSONDecodeError:
        word = random.choice(world_list).upper()
    return word


def splash_screen():
    # Define the layout for the splash screen
    splash_layout = [
        [psg.Image(hangman_img["splash"])],
        [psg.Button("START", font=f"{font_used} 16",
                    border_width=0,
                    key="-START-",
                    button_color="white")]
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
        [psg.Text("", key="-WORD-", font=f"{font_used} 20")],
        [psg.Text("letters used", font=font_used)],
        [psg.Text("", key="-USED-LETTERS-", font=font_used)],
        [psg.Text("lives", font=font_used),
         psg.Text("", key="-LIVES-", font=f"{font_used} 16", text_color="green"),
         psg.Push(),
         psg.Text(str(points), key="-POINTS-", font=f"{font_used} 16", text_color="green"),
         psg.Text("points", font=font_used)],
        [psg.Text("guess a letter:", font=font_used)],
        [psg.Input("", size=(10, 1),
                   enable_events=True,
                   key="-INPUT-")],
        [psg.Button('Submit', visible=False, bind_return_key=True)],
        [psg.Text("", key="-OUTPUT-Msg-", font="Any 10", text_color="yellow")],
        [psg.VPush()]
    ]

    window = psg.Window("Hangman Game", game_layout,
                        size=(300, 570),
                        element_justification="center",
                        finalize=True,
                        no_titlebar=True,
                        grab_anywhere=True,
                        keep_on_top=True)
    return window


def hangman(points=0):
    window = game_window(points)

    # list with alphabet
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # word choice
    word = word_api_or_random()
    print(word)
    # word letters as list
    word_letters = [letter for letter in word]
    # word blanks as list
    word_blanks = ["_"] * len(word)
    # number of lives
    lives = 10
    # letters already used
    guessed_letters = ""

    # Main Loop
    while lives > 0:

        window["-HANGMAN-"].update(hangman_img[lives])
        window["-WORD-"].update("".join(word_blanks), font=f"{font_used} 24")
        window["-USED-LETTERS-"].update(", ".join(guessed_letters))
        window["-LIVES-"].update(lives)

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
                    window["-WORD-"].update("".join(word_blanks), font=f"{font_used} 24")

                    # win condition
                    if "".join(word_blanks) == "".join(word_letters):
                        points += 1
                        window["-POINTS-"].update(str(points))
                        psg.popup(f"YOU WON! Choosing new word in 5s",
                                  font=font_used, keep_on_top=True,
                                  auto_close=True,
                                  auto_close_duration=5)
                        window.close()
                        hangman(points)
                # lost condition
                else:
                    lives = lives - 1
                    window["-OUTPUT-Msg-"].update("Wrong, try again!")
                    window["-HANGMAN-"].update(hangman_img[lives])
                    window["-LIVES-"].update(lives)
                    window["-WORD-"].update("".join(word_blanks), font=f"{font_used} 24")
                    if lives == 0:
                        psg.popup(f"YOU LOST!\n{word} was not guessed.\nChoosing new word in 5s",
                                  font=font_used, keep_on_top=True,
                                  auto_close=True,
                                  auto_close_duration=5)
                        window.close()
                        hangman(points)
            # output if letter already been chosen
            else:
                window["-OUTPUT-Msg-"].update("letter used already !")

    window.close()


if __name__ == '__main__':
    splash_screen()
    hangman()
