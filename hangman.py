#!/usr/bin/env python3

# *** ADD FEATURE - High Score
# ** Make start button nicer
# * Check if is possible to add an image or something while loading from API

import PySimpleGUI as psg
import json
import random
import string
import requests
import webbrowser
from deep_translator import GoogleTranslator
from wordlist import word_list
from lang.localization import localization
from config import version, hangman_img, font_used

psg.theme('black')


def load_settings():
    """Load settings from .json file, if key not found, default language settings will be 'EN'"""

    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
        return settings.get('language', 'EN')


def load_high_scores():
    """Load high scores from the .json file"""
    with open('high_scores.json') as file:
        scores = json.load(file)
    return scores


print(load_high_scores())


def save_settings(settings_dict):
    """Save settings to .json file"""

    with open('settings.json', 'w') as settings_file:
        json.dump(settings_dict, settings_file)


def translate_eng_to_pol(word):
    """Translate any given word to Polish"""

    my_translator = GoogleTranslator(source='english', target='polish')
    result = my_translator.translate(text=word)
    return result


def secret_word_api():
    """Get secret word from API, and choose only words <= 12 characters long"""

    url = "https://random-word-api.herokuapp.com/word"
    response = requests.get(url)
    text = response.json()
    word = text[0]
    if len(word) <= 12:
        return word
    else:
        return secret_word_api()


def word_api_or_random(language):
    """Get secret word from wordlist.py if the API fails for any reason"""

    try:
        word = secret_word_api()
    except (requests.ConnectionError, requests.HTTPError, requests.exceptions.JSONDecodeError):
        word = random.choice(word_list)

    if language == 'EN':
        return word.upper()
    elif language == 'PL':
        return translate_eng_to_pol(word).upper().split(" ")[0]


def check_word_meaning_link(word, language):
    """Create a link to check the meaning of the secret word"""

    if language == "EN":
        query = word.lower().replace(" ", "+")
        url = f'https://www.google.com/search?q={query}+meaning'
        return url
    elif language == "PL":
        query = word.lower().replace(" ", "+")
        url = f'https://www.google.com/search?q={query}+znaczenie'
        return url


def splash_screen(language):
    """Layout for the splash screen window"""

    high_scores = load_high_scores()
    high_scores_string = ""
    for name, score in high_scores.items():
        high_scores_string += f"{name} {score}\n"

    splash_layout = [
        [psg.Push(),
         psg.Button(
             image_filename=hangman_img['settings_icon'],
             pad=(0, 2),
             border_width=0,
             button_color='black',
             enable_events=True,
             key='-SETTINGS-')],
        [psg.Image(hangman_img['splash_logo'])],
        [psg.Button(
            localization[language]['splash.window.start_button'],
            font=(font_used[0], 18),
            border_width=0,
            button_color='white',
            key='-START-')],
        [psg.VPush()],
        [psg.Text("HIGH SCORES:", font=(font_used[0], 11))],
        [psg.Text(high_scores_string, font=(font_used[0], 11))],
        [psg.Text(
            f"{localization[language]['splash.window.version']}: {version}",
            font=(font_used[0], 11))],
        [psg.Text(
            localization[language]['splash.window.github_link'],
            font=(font_used[0], 11),
            text_color='light green',
            enable_events=True,
            key='-LINK-')]
    ]

    splash_window = psg.Window(
        'Splash',
        splash_layout,
        size=(300, 575),
        element_justification='center',
        finalize=True,
        no_titlebar=True,
        grab_anywhere=True,
        keep_on_top=True)

    while True:
        event, values = splash_window.read()
        if event == '-START-':
            break
        elif event == '-SETTINGS-':
            language = settings_window(language)
        elif event == '-LINK-':
            webbrowser.open("https://github.com/paichiwo")

    splash_window.close()
    return language


def settings_window(lang):
    """Layout for the settings window"""

    layout = [
        [psg.Text(
            localization[lang]['settings.window.title'],
            font=(font_used, 12))],
        [psg.Text("")],
        [psg.Text(localization[lang]['settings.window.select_language'])],
        [psg.DropDown(
            ["EN", "PL"],
            default_value=lang,
            text_color='black',
            background_color='light grey',

            key='-LANGUAGE-')],
        [psg.Text("")],
        [psg.Button(localization[lang]['settings.window.save_button'])]
    ]

    window = psg.Window(
        'Settings',
        layout,
        resizable=False,
        finalize=True,
        keep_on_top=True,
        element_justification='c')

    while True:
        event, values = window.read()
        if event == psg.WINDOW_CLOSED:
            break

        elif event == localization[lang]['settings.window.save_button']:
            language = values['-LANGUAGE-']
            save_settings({'language': language})
            window.close()
            return language

    window.close()
    return lang


def game_window(language, points):
    """Layout for the game window"""

    game_layout = [
        # [psg.VPush()],
        [psg.Push(),
         psg.Image(
             hangman_img['close_icon'],
             pad=(0, 4),
             enable_events=True,
             key='-CLOSE-')],
        [psg.VPush()],
        [psg.Image(
            hangman_img[10],
            key='-HANGMAN-')],
        [psg.Text(
            "",
            key='-WORD-',
            font=(font_used[0], 25, 'bold'))],
        [psg.Text(
            localization[language]['game.window.used_letters'],
            font=(font_used[0], 11))],
        [psg.Text(
            "",
            key='-USED-LETTERS-',
            font=(font_used[0], 10),
            text_color='light green')],
        [psg.Text(
            localization[language]['game.window.lives'],
            font=(font_used[0], 11)),
            psg.Text(
                "",
                key='-LIVES-',
                font=(font_used[0], 20),
                text_color='green'),
            psg.Push(),
            psg.Text(
                str(points),
                key='-POINTS-',
                font=(font_used[0], 20),
                text_color='green'),
            psg.Text(
                localization[language]['game.window.points'],
                font=(font_used[0], 11))],
        [psg.Text(
            localization[language]['game.window.guess_letter'],
            font=(font_used[0], 11))],
        [psg.Input(
            "",
            size=(10, 1),
            enable_events=True,
            key='-INPUT-')],
        [psg.Button(
            localization[language]['game.window.submit_button'],
            visible=False,
            bind_return_key=True)],
        [psg.Text(
            "",
            key='-OUTPUT-MSG-',
            font=font_used,
            text_color='yellow')],
        [psg.VPush()]
    ]

    window = psg.Window(
        "Hangman Game",
        game_layout,
        size=(300, 575),
        element_justification='center',
        finalize=True,
        no_titlebar=True,
        grab_anywhere=True,
        keep_on_top=True)

    return window


def hangman(points=0):
    """Hangman game logic"""

    language = load_settings()
    window = game_window(language, points)

    # Alphabet to be used
    alphabet = string.ascii_letters + 'ąęóśłżźćń'
    # Secret word
    word = word_api_or_random(language)
    print(word)
    # Create a Google search link for user to check the meaning of the secret word
    link = check_word_meaning_link(word, language)
    # Word letters as a list
    word_letters = list(word)
    # Word blanks as a list
    word_blanks = ["-"] * len(word)
    # Number of lives
    lives = 10
    # Letters already used
    guessed_letters = ""

    window['-WORD-'].update("".join(word_blanks))
    window['-USED-LETTERS-'].update(localization[language]['game.window.used_letters'].join(guessed_letters))
    window['-HANGMAN-'].update(hangman_img[lives])
    window['-LIVES-'].update(str(lives))

    # Game loop
    while lives > 0:

        event, values = window.read()
        if event in (psg.WIN_CLOSED, '-CLOSE-'):
            break

        # Accepts only one character, which must be from the alphabet
        if len(values['-INPUT-']) > 1 or values['-INPUT-'] not in alphabet:
            # delete last char from input
            window['-INPUT-'].update(values['-INPUT-'][:-1])
        # If enter is pressed
        elif event == localization[language]['game.window.submit_button']:
            user_input = window["-INPUT-"].get().upper()
            window['-INPUT-'].update("")

            # Check if user_input in guessed letters
            if user_input not in guessed_letters:
                guessed_letters += user_input
                window["-USED-LETTERS-"].update(", ".join(guessed_letters))

                # Check if user_input is in the word_letters list
                if user_input in word_letters:
                    window["-OUTPUT-MSG-"].update(localization[language]['game.window.output_msg_good_guess'])

                    # Find indexes of a correctly guessed letter
                    for i, letter in enumerate(word_letters):
                        # and replace blanks with letters
                        if word_letters[i] == user_input:
                            word_blanks[i] = word[i]
                    # Output updated word
                    window["-WORD-"].update("".join(word_blanks))

                    # Win condition
                    if "".join(word_blanks) == "".join(word_letters):
                        points += 1
                        window["-POINTS-"].update(str(points))
                        choice = psg.popup_yes_no(
                            localization[language]['game.window.you_won_message'].format(word),
                            font=font_used, keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        window.close()
                        hangman(points)

                # Loose condition
                else:
                    lives = lives - 1
                    window["-OUTPUT-MSG-"].update(localization[language]['game.window.output_msg_wrong_guess'])
                    window["-HANGMAN-"].update(hangman_img[lives])
                    window["-LIVES-"].update(lives)
                    window["-WORD-"].update("".join(word_blanks))
                    if lives == 0:
                        choice = psg.popup_yes_no(
                            localization[language]['game.window.you_lost_message'].format(word),
                            font=font_used, keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        window.close()
                        return points

            # Letter already been chosen
            else:
                window["-OUTPUT-MSG-"].update(localization[language]['game.window.letter_used_message'])

    window.close()
    return points


def main():
    """Main function that initializes the game"""

    language = load_settings()
    splash_screen(language)
    points = hangman()
    print("Scored points:", points)


if __name__ == '__main__':
    main()
