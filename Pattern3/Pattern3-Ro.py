T = int(input())

for _ in range(T):
    s = input()

    l = len(s)
    acc = ""

    for i in range(0,l):
        acc += s[i]
        suffix = s[(i+1)::]

        l_acc = len(acc)

        if suffix.startswith(acc) and l_acc * suffix.count(acc) == l-l_acc-(l%l_acc) and (l % l_acc == 0 or acc.startswith(s[-(l%l_acc):])):
            break

    print(len(acc))