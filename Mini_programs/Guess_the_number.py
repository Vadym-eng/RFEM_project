from random import *

a = randint(0, 101)
print("Добро пожаловать в числовую угадайку")
while True:
    b = int(input())
    if b == a:
        print("Вы угадали, поздравляем!")
        a = randint(0, 101)
    elif b < a:
        print("Слишком мало, попробуйте еще раз")
    elif b > a:
        print("Слишком много, попробуйте еще раз")
