#!/usr/bin/env python3

# Hangman_GUI main game file with application layout and game logic

from Wordlist import world_list
import PySimpleGUI as sg
import random

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
sg.theme("black")

# Define the layout for the splash screen
splash_layout = [
    [sg.Image(hangman_img["splash"])],
    [sg.Button("START", font=font_used,
               border_width=0,
               key="-START-",
               button_color="white")]
]

# Create the splash screen window
splash_window = sg.Window('Splash', splash_layout,
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

# Main Game Layout
game_layout = [
    [sg.VPush()],
    [sg.Push(), sg.Image("img/close.png",  # Close button
                         pad=0, enable_events=True, key="-CLOSE-")],
    [sg.VPush()],
    [sg.Image(hangman_img[0], key="-HANGMAN-")],
    [sg.Text("", key="-WORD-", font="Young 20")],
    [sg.Text("letters used", font=font_used)],
    [sg.Text("", key="-USED-LETTERS-", font=font_used)],
    [sg.Text("lives", font=font_used),
     sg.Text("", key="-LIVES-", font="Young 16", text_color="green"),
     sg.Push(),
     sg.Text("0", key="-POINTS-", font="Young 16", text_color="green"),
     sg.Text("points", font=font_used)],
    [sg.Text("Guess a letter:", font=font_used)],
    [sg.Input("", size=(10, 1),
              enable_events=True,
              key="-INPUT-")],
    [sg.Button('Submit', visible=False, bind_return_key=True)],
    [sg.Text("", key="-OUT-", font="Any 10", text_color="yellow")],
    [sg.VPush()]
]

window = sg.Window("Hangman Game", game_layout,
                   size=(300, 570),
                   element_justification="center",
                   finalize=True,
                   no_titlebar=True,
                   grab_anywhere=True,
                   keep_on_top=True)


def hangman():

    # list with alphabet
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z']
    # word choice
    word = random.choice(world_list).upper()
    # word letters as list
    word_letters = [letter for letter in word]
    # word blanks as list
    word_blanks = ["_"] * len(word)
    # number of lives
    lives = 10
    # points
    points = 0
    # letters already used
    guessed_letters = ""

    # Main Loop
    while lives > 0:

        window["-HANGMAN-"].update(hangman_img[lives])
        window["-WORD-"].update("".join(word_blanks), font="Young 24")
        window["-USED-LETTERS-"].update(", ".join(guessed_letters))
        window["-LIVES-"].update(lives)

        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-"):
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
                    window["-OUT-"].update("Great guess, letter found")

                    # find indexes of correctly guessed letter
                    for i, letter in enumerate(word_letters):
                        # and replace blanks with letters
                        if word_letters[i] == user_input:
                            word_blanks[i] = word[i]
                    # output updated word
                    window["-WORD-"].update("".join(word_blanks), font="Young 24")

                    # win condition
                    if "".join(word_blanks) == "".join(word_letters):
                        points += 1
                        window["-OUT-"].update("Fantastic, You Won!")
                        window["-POINTS-"].update(str(points))
                        sg.popup("YOU WON, Choosing new word...", font=font_used, keep_on_top=True)
                        hangman()
                # lost condition
                else:
                    lives = lives - 1
                    window["-OUT-"].update("Wrong, Try again!")
                    window["-HANGMAN-"].update(hangman_img[lives])
                    window["-LIVES-"].update(lives)
                    window["-WORD-"].update("".join(word_blanks), font="Young 24")
                    if lives == 0:
                        window["-OUT-"].update("You lost")
                        sg.popup(f"YOU LOST \nword: {word} was not guessed\nChoosing new word",
                                 font=font_used, keep_on_top=True)
                        hangman()
            # output if letter already been chosen
            else:
                window["-OUT-"].update("Letter used already !")

    window.close()


if __name__ == '__main__':
    hangman()
