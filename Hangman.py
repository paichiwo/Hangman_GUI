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

