c = int(input())
n = [input() for _ in range(c)]
cor = set()
cor1 = []


def rond(n):
    if n % 1 >= 0.5:
        return round(n + 0.1)
    else:
        return round(n)


for i in n:
    if "Correct" in i:
        cor.add(i)
        cor1.append(i)
if len(cor) != 0:
    print(f"Верно решили {len(cor)} учащихся")
    print(f"Из всех попыток {rond((len(cor1)/c)*100)}% верных")
else:
    print("Вы можете стать первым, кто решит эту задачу")
