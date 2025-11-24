import random
import os
from typing import List, Set

# Константы и данные

# Значение MAX_ATTEMPTS исправлено с 6 на 7, тк даже если веревочка уже есть у висельника на рисунке, то ост частей от
# человека остается 7 (1 голова-кружочек + 2 палки вниз как тело + 2 руки + 2 ноги), что являются графическим отображением
# максимального возможного количества ошибок пользователя.
MAX_ATTEMPTS = 7
WORDS = [
    "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА", 
    "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА", 
    "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ", 
    "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
# я добавила еще слов, чтобы поиграть можно было подольше
    "КОДИРОВАНИЕ", "ТЕСТИРОВАНИЕ", "ПАРАМЕТР", "ИНТЕРФЕЙС", "БАГ",
    "ОПТИМИЗАЦИЯ", "МОДУЛЬ", "ДОКУМЕНТАЦИЯ", "ДЕБАГ", "КОМПИЛЯТОР",
    "ОСНОВА", "ДАННЫЕ", "РЕЗУЛЬТАТ", "ОБЪЕКТ", "МОДЕЛЬ", "ПРОЕКТ",
    "СИСТЕМА", "СИНТАКСИС", "ЛОГИКА", "ДЕФИНИЦИЯ", "МОДИФИКАТОР",
    "КОМАНДА", "ПРОГРАММА", "ИНТЕРПРЕТАТОР", "КЛАСС", "ОБЛАСТЬ",
    "ПЕРЕМЕННАЯ", "УСЛОВИЕ", "СТЕК", "ГЛОБАЛЬНЫЙ", "ЛОГИЧЕСКИЙ",
    "ПАРСЕР", "ПОСТООБРОТКА", "ФАЙЛ", "РЕКУРСИЯ", "МЕНЕДЖЕР"
]

stats = {
    "games_played": 0,
    "games_won": 0,
    "total_score": 0,
    "best_score": 0
}

def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")
    
    # Загрузка статистики
    global stats
    
    while True:
        # Выбор случайного слова
        secret_word = choose_random_word(WORDS)
        guessed_letters = set()
        attempts_left = MAX_ATTEMPTS
        game_won = False
        
        # Игровой цикл
        while attempts_left > 0:
            # Отрисовка текущего состояния игры
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            
            # Ввод буквы
            # TODO: обработать ввод буквы (используй get_user_guess)
            letter = get_user_guess(guessed_letters, secret_word)
            
            # Проверка угадана ли буква
            # TODO: добавить реализацию проверки буквы (используй get_user_guess)
            guessed_letters.add(letter)

            if letter not in secret_word:
                attempts_left -= 1
            
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            # score = TODO: получи с помощью функции счет (используй calculate_score)
            score = calculate_score(secret_word, attempts_left)
            # print(f"Ваш счет: {score}")
            print(f"Ваш счет: {score}")
            # TODO: обнови статистику (используй update_stats)
            update_stats(won=True, score=score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            # TODO: обнови статистику (используй update_stats)
            update_stats(won=False, score=0)
            draw_gallows(0)
        
        show_stats()
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)

def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""
    # TODO: реализовать генерацию в зависимости от угаданных букв
    masked_word = ['_'] * len(secret_word)
    list_for_score_of_guessed_letters = []
    for indx, letter in enumerate(secret_word):
        if letter in guessed_letters:
            masked_word[indx] = letter
            list_for_score_of_guessed_letters.append(letter)
        else:
            masked_word[indx] = '_'
    return ' '.join(masked_word)

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    # TODO: реализовать отрисовку (нужно вызвать print)
    # Подсказка:
    # """
        # --------
        # |      |
        # |      O
        # |     \\|/
        # |      |
        # |     / \\
        # -
        # """

    matrix_hangman = [
        ['-', '-', '-', '-', '-', '-', '-', '-', '\n'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', '\n'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'],
        ['-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]

    if (attempts_left == 6):
        matrix_hangman[2][7] = 'O'
    elif (attempts_left == 5):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
    elif (attempts_left == 4):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
        matrix_hangman[4][7] = '|'
    elif (attempts_left == 3):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
        matrix_hangman[4][7] = '|'
        matrix_hangman[3][8] = '/'
    elif (attempts_left == 2):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
        matrix_hangman[4][7] = '|'
        matrix_hangman[3][8] = '/'
        matrix_hangman[3][6] = '\\'
    elif (attempts_left == 1):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
        matrix_hangman[4][7] = '|'
        matrix_hangman[3][8] = '/'
        matrix_hangman[3][6] = '\\'
        matrix_hangman[5][6] = '/'
    elif (attempts_left == 0):
        matrix_hangman[2][7] = 'O'
        matrix_hangman[3][7] = '|'
        matrix_hangman[4][7] = '|'
        matrix_hangman[3][8] = '/'
        matrix_hangman[3][6] = '\\'
        matrix_hangman[5][6] = '/'
        matrix_hangman[5][8] = '\\'

    for row in matrix_hangman:
        print(''.join(row))
    
def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""
    # TODO: проверять, что пользователь ввел только одну букву, что он не вводил уже эту букву и тд
    # Подсказка: не забывай про регистр
    while True:
    letter_users = input("Введите предполагаемую букву: ").upper()
    if len(letter_users) == 1:
        if letter_users == 'Ё' or 'А' <= letter_users <= 'Я':
            if letter_users in guessed_letters:
                print("Такая буква уже была испробована/введена. Попробуйте другую.")
                continue
            else:
                guessed_letters.add(letter_users)
        else:
            print("Вы можете вводить только русские буквы. Ничего кроме.")
            continue
    else:
        print("Вы можете ввести только одну букву за одну попытку.")
        continue
    return letter_users
    
def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""
    # TODO: реализовать проверку
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    # TODO: необходимо, используя длину secret_word и количество попыток, посчитать счет
    score = attempts_left * len(secret_word)
    list_score_every_game.append(score)
    return score
    # Я не особо поняла, что это вообще за счет, а в правилах игры на просторах инета пишут про условное назначение
    # баллов за верно отгаданные буквы, так что введу свое обозначение формальное чисто для этой работы:
    # счет за 1 игру это выражение вида Х * У, где Х - количество попыток, а У - количество букв в загаданном слове.    
    
def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats
    # TODO: необходимо обновить stats
    stats["games_played"] += 1
    if won:
        stats["games_won"] += 1
    stats["total_score"] += score
    if list_score_every_game:
        stats["best_score"] = max(list_score_every_game)
    else:
        stats["best_score"] = score
    
def show_stats():
    """Отображение статистики"""
    global stats
    # win_percentage = TODO: посчитай на основе имеющейся статистики процент выигрыша
    win_percentage = (stats["games_won"] / stats["games_played"]) * 100
    # average_score = TODO: посчитай на основе имеющейся статистики средний счет
    average_score = stats["total_score"] / stats["games_played"]
    else:
        win_percentage = 0
        average_score = 0
    
    print("\n=== Статистика ===")
    # print(f"Всего игр: {TODO: количество игр}")
    print(f"Количество игр: {stats["games_played"]}")
    # print(f"Побед: {TODO: количество побед} ({win_percentage:.1f}%)")
    print(f"Побед: {win_percentage}%")
    if list_score_every_game:
        stats["best_score"] = max(list_score_every_game)
    else:
        stats["best_score"] = 0
    # print(f"Лучший счет: {TODO: выведи лучший счет}")
    print(f"Лучший счет: {stats["best_score"]}")
    # TODO: выведи средний счет, если была хотя бы одна победа
    if stats["games_won"] > 0:
        print(f"Средний счет: {average_score}")

if __name__ == "__main__":
    main()
