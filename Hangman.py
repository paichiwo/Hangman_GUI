# Hangman_GUI main game file

from Wordlist import world_list
import PySimpleGUI as sg
import random

# Dictionary with all images used in the game
hangman_img = {
    0: "img/Hangman_00.png",
    1: "img/Hangman_01.png",
    2: "img/Hangman_02.png",
    3: "img/Hangman_03.png",
    4: "img/Hangman_04.png",
    5: "img/Hangman_05.png",
    6: "img/Hangman_06.png",
    7: "img/Hangman_07.png",
    8: "img/Hangman_08.png",
    9: "img/Hangman_09.png",
    10: "img/Hangman_10.png"
}

# Install "Young.ttf" (main folder) for best experience, but app will still work without it :)
font_used = "Young"
# Create window layout with PySimpleGUI
sg.theme("black")
layout = [
    [sg.Image(hangman_img[0], key="-HANGMAN-")],
    [sg.Text("", key="-WORD-", font="Young 20")],
    [sg.Text("letters used", font=font_used)],
    [sg.Text("", key="-USED-LETTERS-", font=font_used)],
    [sg.Text("lives", font=font_used),
     sg.Text("10", key="-LIVES-", font="Young 16", text_color="green"),
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

window = sg.Window("Hangman Game", layout,
                   size=(300, 550),
                   element_justification="center",
                   finalize=True)