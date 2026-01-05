N, V, P = map(int, input().split())

buns = []
for i in range(N):
    buns.append(input())

showcase = []
i = 0

# первые булочки в витрину
while i < V and i < N:
    showcase.append(buns[i])
    i += 1

# покупатели
for _ in range(P):
    a, b, c = input().split()
    result = "-"

    if a in showcase:
        result = a
        showcase.remove(a)
    else:
        if b in showcase:
            result = b
            showcase.remove(b)
        else:
            if c in showcase:
                result = c
                showcase.remove(c)

    if result != "-" and i < N:
        showcase.append(buns[i])
        i += 1

    print(result)
