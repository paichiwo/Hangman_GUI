import string
import webbrowser
import PySimpleGUI as psg
from hangman.config import hangman_img, font_used
from lang.localization import localization
from hangman.helpers import load_settings, word_api_or_word_list, check_word_meaning, resource_path, update_high_scores
from hangman.GUI import splash_screen, game_window


def hangman(points=0):
    """Hangman game logic"""

    language = load_settings()
    window = game_window(language, points)

    # Alphabet to be used
    alphabet = string.ascii_letters + "ąęóśłżźćń"
    # Secret word
    word = word_api_or_word_list(language)
    print(word)
    # Create a Google search link for user to check the meaning of the secret word
    link = check_word_meaning(word, language)
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
    window['-HANGMAN-'].update(resource_path(hangman_img[lives]))
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
            user_input = window['-INPUT-'].get().upper()
            window['-INPUT-'].update("")

            # Check if user_input in guessed letters
            if user_input not in guessed_letters:
                guessed_letters += user_input
                window['-USED-LETTERS-'].update(", ".join(guessed_letters))

                # Check if user_input is in the word_letters list
                if user_input in word_letters:
                    window['-OUTPUT-MSG-'].update(localization[language]['game.window.output_msg_good_guess'])

                    # Find indexes of a correctly guessed letter
                    for i, letter in enumerate(word_letters):
                        # and replace blanks with letters
                        if word_letters[i] == user_input:
                            word_blanks[i] = word[i]
                    # Output updated word
                    window['-WORD-'].update("".join(word_blanks))

                    # Win condition
                    if "".join(word_blanks) == "".join(word_letters):
                        points += 1
                        window['-POINTS-'].update(str(points))
                        choice = psg.popup_yes_no(
                            localization[language]['game.window.you_won_message'].format(word),
                            font=(font_used, 10),
                            keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        window.close()
                        hangman(points)

                # Loose condition
                else:
                    lives = lives - 1
                    window['-OUTPUT-MSG-'].update(localization[language]['game.window.output_msg_wrong_guess'])
                    window['-HANGMAN-'].update(resource_path(hangman_img[lives]))
                    window['-LIVES-'].update(lives)
                    window['-WORD-'].update("".join(word_blanks))
                    if lives == 0:
                        choice = psg.popup_yes_no(
                            localization[language]['game.window.you_lost_message'].format(word),
                            font=(font_used, 10),
                            keep_on_top=True)
                        if choice == "Yes":
                            webbrowser.open(link)
                        name = psg.popup_get_text(
                            localization[language]['game.window.enter_name_message'],
                            localization[language]['game.window.enter_name_title'],
                            font=font_used,
                            keep_on_top=True)
                        if name:
                            update_high_scores(name, points)

                        window.close()
                        splash_screen(language)
                        hangman()

            # Letter already been chosen
            else:
                window['-OUTPUT-MSG-'].update(localization[language]['game.window.letter_used_message'])

    window.close()


def main():
    """Main function that initializes the game"""

    psg.theme('black')
    language = load_settings()
    splash_screen(language)
    hangman()


if __name__ == '__main__':
    main()
