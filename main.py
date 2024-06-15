import random
from copy import deepcopy

from numpy import cos, int8, int16, int32, int64, tan, uint8, uint16, uint32, uint64
from numpy import sin as np_sin

from hangmanwordbank import HANGMANPICS, animal_words

BACKUP_WORDS = deepcopy(animal_words)
WORD_LIST_PATH = "word_list.txt"
HANGMAN_TITLE_PATH = "title.txt"


def display_title(file):
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        raise Exception("An error occurred while trying to access file...Exiting application.")


def display_menu():
    print("1. Enter personal details")
    print("2. Display personal details")
    print("3. Start playing the game")
    print("4. Add words to text file")
    print("5. Quit game")
    choice = input("Enter option: ")
    print(f"Option chosen: {choice}")
    return choice


def retrieve_word_list(words_file_path):
    try:
        with open(words_file_path, "r") as f:
            words = f.read().split("\n")

    except FileNotFoundError:
        print("Words file not found...backup words will be used instead")
        words = deepcopy(BACKUP_WORDS)

    except IOError:
        print("An error occurred while trying to fetch the word...Exiting application")
    return words


def start_game(words):
    """
    Hangman implementation
    """
    max_incorrect_guesses = len(HANGMANPICS) - 1
    incorrect_guesses = -1
    word_to_guess = list(words[random.randint(0, len(words) - 1)])
    word_to_guess_masked = ["*" for char in word_to_guess]
    already_guessed = []

    game = True
    win_game = False

    while game:
        if already_guessed:
            print(f'Already guessed: {', '.join(already_guessed)}')
        print(f'Word to guess: {''.join(word_to_guess_masked)}')
        guess_char = input("Guess a character or a word: ")

        if guess_char in word_to_guess and guess_char not in already_guessed:
            char_indexes = [i for i, c in enumerate(word_to_guess) if c == guess_char]
            for index in char_indexes:
                word_to_guess_masked[index] = guess_char
        elif guess_char not in word_to_guess and guess_char not in already_guessed:
            incorrect_guesses += 1
            print(HANGMANPICS[incorrect_guesses])

        if guess_char not in already_guessed:
            already_guessed.append(guess_char)

        if incorrect_guesses == max_incorrect_guesses:
            game = False

        if "".join(word_to_guess) == "".join(word_to_guess_masked):
            game = False
            win_game = True

    if win_game:
        print("YOU WON")
    else:
        print("GAME OVER")
    print(f'The word was: {''.join(word_to_guess)}')


def add_words_to_text_file(word_list_file):
    dialogue = True
    words_to_add = []

    while dialogue:
        word = input("Enter word (enter -1 to exit): ")
        if word != "-1":
            words_to_add.append(word)
        else:
            dialogue = False

    with open(word_list_file, "r+") as f:
        words_from_file = f.read().split("\n")
        unique_words = [word for word in words_to_add if word not in words_from_file]
        new_words = words_from_file + unique_words
        f.seek(0)
        f.write("\n".join(new_words))
    print(f'Success. Words added to {word_list_file}: {', '.join(unique_words)}')


def enter_personal_details():
    name = input("Name: ")
    surname = input("Surname: ")
    personal_details = {"name": name, "surname": surname}
    return personal_details


def display_personal_details(details):
    if details:
        print("--- Your personal details ---")
        for k, v in details.items():
            print(f"{k}: {v}")
    else:
        print("--- No personal details found ---")


def main():
    display_title(HANGMAN_TITLE_PATH)
    words = retrieve_word_list(WORD_LIST_PATH)
    personal_details = {}

    execution = True
    while execution:
        choice = display_menu()
        match choice:
            case "1":
                personal_details = enter_personal_details()
            case "2":
                display_personal_details(personal_details)
            case "3":
                start_game(words)
            case "4":
                add_words_to_text_file(WORD_LIST_PATH)
            case "5":
                execution = False
    print("Exiting program...")


if __name__ == "__main__":
    # main()
    dct = {"name": "luke"}
    lst = ["test"]

    print(f'{dct['name']}')
