import json
import os
import random
import sys
import requests
from deep_translator import GoogleTranslator



def resource_path(relative_path):
    """PyInstaller requirement,
    Get an absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_settings():
    """Load settings from .json file, if key not found, default language settings will be 'EN'"""

    with open(resource_path('../settings.json'), 'r') as settings_file:
        settings = json.load(settings_file)
        return settings.get('language', 'EN')


def save_settings(settings_dict):
    """Save settings to .json file"""

    with open(resource_path('../settings.json'), 'w') as settings_file:
        json.dump(settings_dict, settings_file)


def load_high_scores():
    """Load high scores from the .json file"""

    with open(resource_path('../high_scores.json'), 'r') as file:
        scores = json.load(file)
    return scores


def update_high_scores(name, score):
    """Update high scores in the .json file"""

    scores = load_high_scores()

    # If there are already three high scores and the new score is lower than the lowest score, return
    if len(scores) >= 3 and score <= min(scores.values()):
        return
    # Update the high scores with the new score
    scores[name] = score
    # Keep only the top three scores
    top_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3])
    # Save the updated scores to the file
    with open(resource_path('../high_scores.json'), 'w') as file:
        json.dump(top_scores, file)


def create_high_scores_string():
    """Create a string to display on the splash screen"""

    high_scores = load_high_scores()
    high_scores_string = ""
    for name, score in high_scores.items():
        high_scores_string += f"{name}  {score}\n"
    return high_scores_string


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


def secret_word_from_list():
    """Get word from word_list.json"""

    with open('word_list.json', 'r') as json_file:
        json_data = json_file.read()
    word_dict = json.loads(json_data)
    word_list = word_dict['word_list']

    return word_list


def word_api_or_word_list(language):
    """Get secret word from wordlist.py if the API fails for any reason"""

    try:
        word = secret_word_api()
    except (requests.ConnectionError, requests.HTTPError, requests.exceptions.JSONDecodeError):
        word = random.choice(secret_word_from_list())

    if language == 'EN':
        return word.upper()
    elif language == 'PL':
        print(word)
        return translate_eng_to_pol(word).upper().split(" ")[0]


def check_word_meaning(word, language):
    """Create a link to check the meaning of the secret word"""

    if language == "EN":
        query = word.lower().replace(" ", "+")
        url = f'https://www.google.com/search?q={query}+meaning'
        return url
    elif language == "PL":
        query = word.lower().replace(" ", "+")
        url = f'https://www.google.com/search?q={query}+znaczenie'
        return url