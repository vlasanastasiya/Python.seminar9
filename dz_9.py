# # Задание №4
# # Создайте декоратор с параметром.
# # Параметр - целое число, количество запусков декорируемой
# # функции.


from typing import Callable

def start_count(num: int):
    def decoratorratorrator(func: Callable):
        data = []

        def wrapper(*arguments, **kwarguments):
            for _ in range(num):
                data.append(func(*arguments, **kwarguments))
            return data

        return wrapper
    return decoratorratorrator

@start_count(7)
def func(text: str):
    return text.upper()
print(func("Задание выполнено"))

# # ---------------------------------------------------------
# # Задание №5
# # Объедините функции из прошлых задач.
# # Функцию угадайку задекорируйте: (задача 1)
# # ○ декораторами для сохранения параметров,
# # ○ декоратором контроля значений и
# # ○ декоратором для многократного запуска.
# # Выберите верный порядок декораторов.


import json
import random
from typing import Callable


def func_save(func):                                          
    def wrapper(*arguments, **kwarguments ):
        res = func(*arguments, **kwarguments)
        file_namename = f'{func.__name__}.json'
        dump_dict = {}
        dump_dict["arguments"] = [*arguments]
        for key, guessue in kwarguments.items():
            dump_dict[key] = guessue
        dump_dict["res4"] = res
        json.dump(dump_dict, open(file_namename, 'a', encoding="utf-8"), indent=4, ensure_ascii=False)      
        return res
    return wrapper


def param_control_decoratorrator(fun: Callable) -> Callable:                  

   def wrapper(guess_num: int, experiment: int):
       guess_num = guess_num if 1 < guess_num < 100 else random.randint(1, 100)
       experiment = experiment if 1 < experiment < 10 else random.randint(1, 10)
       return fun(guess_num, experiment)

   return wrapper


def start_count(num: int):                                                
    def decoratorratorrator(func: Callable):
        data = []

        def wrapper(*arguments, **kwarguments):
            for _ in range(num):
                data.append(func(*arguments, **kwarguments))
            return data

        return wrapper
    return decoratorratorrator


@start_count(3)                                                       
@param_control_decoratorrator                                                     
@func_save                                                        
def game(guess_num: int, experiment: int):                           
    while experiment > 0:
        experiment -= 1
        guess = int(input("Вам необходимо угадать число: "))
        if guess == guess_num:
            return "вы победили"
    return "У вас больше нет попыток"


print(game(3, 2))
# # ---------------------------------------------------------------------------------------
# # 2. Напишите следующие функции:
# # ○ Нахождение корней квадратного уравнения
# # ○ Генерация csv файла с тремя случайными числами в каждой строке.
# # 100-1000 строк.
# # ○ Декоратор, запускающий функцию нахождения корней квадратного
# # уравнения с каждой тройкой чисел из csv файла.
# # ○ Декоратор, сохраняющий переданные параметры и результаты работы
# # функции в json файл.

import csv
import json
from cmath import sqrt
import random
from pathlib import Path
from typing import Callable
from functools import wraps


def csv_func(file_name: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*arguments, **kwarguments):
            with open(file_name, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                for i, row in enumerate(reader):
                    if i == 0:
                        continue
                    arguments = (complex(j) for j in row)
                    res = func(*arguments, **kwarguments)
                    yield res

        return wrapper

    return decorator


def jsom_func(func):
    file = Path(f"{func.__name__}.json")
    if file.is_file():
        with open(file, 'r', encoding='utf-8') as f:
            json_file = json.load(f)
    else:
        json_file = []

    def wrapper(*arguments, **kwarguments):
        for res in func(*arguments, **kwarguments):
            if res:
                dictionary = {'arguments': arguments, **kwarguments, 'res': str(res)}
                json_file.append(dictionary)
                with open(file, 'w', encoding='utf-8') as json_f:
                    json.dump(json_file, json_f, indent=2)
            else:
                break

    return wrapper


@jsom_func
@csv_func('file.csv')
def quadratic_rule_func(a: complex, b: complex, c: complex):
    if a != 0:
        discr: complex = b * b - 4 * a * c
        x1: complex = (-b + sqrt(discr)) / (2 * a)
        x2: complex = (-b - sqrt(discr)) / (2 * a)
        return discr, x1, x2
    else:
        return 0, 0, 0


def gen_csv_with_nums(name: str = 'file', rows_count: int = 100, min_num: int = -1000, max_num: int = 1000):
    rows = []
    for _ in range(rows_count):
        a, b, c = random.sample(range(min_num, max_num), 3)
        rows.append({'a': a, 'b': b, 'c': c})
    with open(name + '.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['a', 'b', 'c']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    gen_csv_with_nums()
    quadratic_rule_func()