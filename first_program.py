a = [set(input())for i in range(int(input()))]
n = a[0]
for i in a:
    n.intersection_update(i)
print(*sorted(n))
