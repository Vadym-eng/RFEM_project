import random

print("Привет Мир, я магический шар, и я знаю ответ на любой твой вопрос.")
name = input("Как тебя зовут?")
print(f"Привет, {name.title()}. Давай начнем ?")
print("Что бы ты хотел узнать? Задай вопрос так, чтобы вопрос был 'да' или 'нет':")

while True:
    print(input())
    print(random.choice(
        [
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо, да",
            "Можешь быть уверен в этом",
            "Мне кажется - да",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят - да",
            "Да",
            "Пока неясно, попробуй снова",
            "Спроси позже",
            "Лучше не рассказывать",
            "Сейчас нельзя предсказать",
            "Сконцентрируйся и спроси снова",
            "Даже не думай",
            "Мой ответ - нет",
            "По моим данным - нет",
            "Перспективы не очень хорошие",
            "Весьма сомнительно",
        ]
    ))
    print("Хочешь еще что-нибудь спросить? Напечатай 'да' или 'нет'.")
    more = input()
    if more.lower() == "нет":
        break
print("Возвращайся если возникнут вопросы!")