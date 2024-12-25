from random import *

digits = "0123456789"
lowercase_letters = "abcdefghijklmnopqrstuvwxy"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
punctuation = "!#$%&*+-=?@^_"
chars = ""
cntPw = int(input("Укажите количество паролей для генерации:"))
lenPw = int(input("Укажите длину одного пароля:"))
digOn = input("Включать ли цифры 0123456789? (да/нет)")
ABCon = input("Включать ли прописные буквы ABCDEFGHIJKLMNOPQRSTUVWXYZ? (да/нет)")
abcOn = input("Включать ли строчные буквы abcdefghijklmnopqrstuvwxyz? (да/нет)")
chOn = input("Включать ли символы !#$%&*+-=?@^_? (да/нет)")
excOn = input("Исключать ли неоднозначные символы il1Lo0O? (да/нет)")
if digOn.lower() == "да":
    chars += digits
if ABCon.lower() == "да":
    chars += uppercase_letters
if abcOn.lower() == "да":
    chars += lowercase_letters
if chOn.lower() == "да":
    chars += punctuation
if excOn.lower() == "да":
    for c in "il1Lo0O":
        chars.replace(c, "")


def generate_password(length, chars):
    password = ""
    for i in range(length):
        password += choice(chars)
    return password


for i in range(cntPw):
    print(generate_password(lenPw, chars))
