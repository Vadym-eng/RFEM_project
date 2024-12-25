direction = input("Выберите направление: шифрование / дешифрование")
lenguag = input("Выберите язык: русский / английский")
step_shift = int(input("Выберите шаг сдвига: co сдвигом вправо"))
text = input("Введите текст")
eng_lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
eng_upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rus_lower_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
rus_upper_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def caesar(direction, language, step, text):
    new_text = ""
    for i in range(len(text)):
        if language[:3] == "рус":
            alphas = 32
            low_alphabet = rus_lower_alphabet
            upp_alphabet = rus_upper_alphabet
        if language[:3] == "анг":
            alphas = 26
            low_alphabet = eng_lower_alphabet
            upp_alphabet = eng_upper_alphabet
        if text[i] in low_alphabet:
            place = low_alphabet.find(text[i])
        elif text[i] in upp_alphabet:
            place = upp_alphabet.find(text[i])
        if direction[:3] == "шиф":
            index = (place + step) % alphas
        elif direction[:3] == "деш":
            index = (place - step) % alphas
        if text[i] in upp_alphabet:
            new_text += upp_alphabet[index]
        elif text[i] in low_alphabet:
            new_text += low_alphabet[index]
        else:
            new_text += text[i]
    print(new_text)


caesar(direction, lenguag, step_shift, text)

# берет кольво букв в слове и переставляет эти буквы на количество этих же букв
"""text = input()
eng_lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
eng_upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chifr_text = ""
alphas = 26
text = text.split()
for i in range(len(text)):
    for j in range(len(text[i])):
        if text[i][j].isalpha():
            couter = 0
            for u in text[i]:
                if u.isalpha():
                    couter += 1
            if text[i][j] in eng_lower_alphabet:
                nomer = eng_lower_alphabet.find(text[i][j])
                chifr_text += eng_lower_alphabet[((nomer+couter)%alphas)]
            elif text[i][j] in eng_upper_alphabet:
                nomer = eng_upper_alphabet.find(text[i][j])
                chifr_text += eng_upper_alphabet[((nomer+couter)%alphas)]
        else:
            chifr_text += text[i][j]
    chifr_text += " "
    
print(chifr_text)"""
