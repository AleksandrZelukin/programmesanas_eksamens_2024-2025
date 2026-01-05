import sys
from collections import deque, defaultdict

def main():
    input = sys.stdin.readline

    N, V, P = map(int, input().split())

    baked = [input().strip() for _ in range(N)]
    buyers = [input().split() for _ in range(P)]

    # Vitrīna kā rinda
    showcase = deque()
    count = defaultdict(int)

    idx = 0  # nākamā bulciņa no izceptajām

    # Sākotnēji piepildām vitrīnu
    while idx < N and len(showcase) < V:
        b = baked[idx]
        showcase.append(b)
        count[b] += 1
        idx += 1

    out = []

    for p1, p2, p3 in buyers:
        bought = "-"

        for pref in (p1, p2, p3):
            if count[pref] > 0:
                bought = pref
                break

        if bought != "-":
            # Izņemam vienu šāda veida bulciņu no vitrīnas
            for i in range(len(showcase)):
                if showcase[i] == bought:
                    showcase.remove(bought)
                    break

            count[bought] -= 1

            # Pievienojam nākamo izcepto, ja ir
            if idx < N:
                new_bun = baked[idx]
                showcase.append(new_bun)
                count[new_bun] += 1
                idx += 1

        out.append(bought)

    print("\n".join(out))


if __name__ == "__main__":
    main()
