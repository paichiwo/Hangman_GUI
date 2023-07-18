import webbrowser
import PySimpleGUI as psg
from hangman_data.config import hangman_img, font_used, version
from hangman_data.helpers import create_high_scores_string, resource_path, save_settings
from lang.localization import localization


def splash_screen(language):
    """Layout for the splash screen window"""

    high_scores_string = create_high_scores_string()

    splash_layout = [
        [psg.Push(),
         psg.Button(
             image_filename=resource_path(hangman_img['settings_icon']),
             pad=(0, 5),
             border_width=0,
             button_color='black',
             enable_events=True,
             key='-SETTINGS-')],
        [psg.Image(resource_path(hangman_img['splash_logo']))],
        [psg.Button(
            localization[language]['splash.window.start_button'],
            font=(font_used, 18),
            border_width=0,
            button_color='white',
            key='-START-')],
        [psg.VPush()],
        [psg.Text(
            "HIGH SCORES",
            font=(font_used, 12, 'bold'),
            text_color='light green')],
        [psg.Text(
            high_scores_string,
            font=(font_used, 11))],
        [psg.Text(
            f"{localization[language]['splash.window.version']}: {version}",
            font=(font_used, 11))],
        [psg.Text(
            localization[language]['splash.window.github_link'],
            font=(font_used, 11),
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
        grab_anywhere=True)

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
        [psg.Text(
            localization[lang]['settings.window.select_language'],
            font=(font_used, 11))],
        [psg.DropDown(
            ["EN", "PL"],
            default_value=lang,
            font=(font_used, 12),
            text_color='black',
            background_color='light grey',
            key='-LANGUAGE-')],
        [psg.Text("")],
        [psg.Button(
            localization[lang]['settings.window.save_button'],
            font=(font_used, 11),
            button_color='white',
            border_width=0)]
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
             resource_path(hangman_img['close_icon']),
             pad=(0, 4),
             enable_events=True,
             key='-CLOSE-')],
        [psg.VPush()],
        [psg.Image(
            resource_path(hangman_img[10]),
            key='-HANGMAN-')],
        [psg.Text(
            "",
            key='-WORD-',
            font=(font_used, 25, 'bold'))],
        [psg.Text(
            localization[language]['game.window.used_letters'],
            font=(font_used, 11))],
        [psg.Text(
            "",
            key='-USED-LETTERS-',
            font=(font_used, 10),
            text_color='light green')],
        [psg.Text(
            localization[language]['game.window.lives'],
            font=(font_used, 11)),
            psg.Text(
                "",
                key='-LIVES-',
                font=(font_used, 20),
                text_color='green'),
            psg.Push(),
            psg.Text(
                str(points),
                key='-POINTS-',
                font=(font_used, 20),
                text_color='green'),
            psg.Text(
                localization[language]['game.window.points'],
                font=(font_used, 11))],
        [psg.Text(
            localization[language]['game.window.guess_letter'],
            font=(font_used, 11))],
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
        grab_anywhere=True)

    return window
